
import ast
import json
import requests
import numpy as np
from base64 import b64encode
from struct import pack

from django.db import models
from django.core.urlresolvers import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.main.models import Configuration
from devices.rc import api
from .utils import RCFile

# Create your models here.

LINE_TYPES = (
    ('none', 'Not used'),
    ('tr', 'Transmission/reception selector signal'),
    ('tx', 'A modulating signal (Transmission pulse)'),
    ('codes', 'BPSK modulating signal'),
    ('windows', 'Sample window signal'),
    ('sync', 'Synchronizing signal'),
    ('flip', 'IPP related periodic signal'),
    ('prog_pulses', 'Programmable pulse'),
    ('mix', 'Mixed line'),
    )


SAMPLING_REFS = (
    ('none', 'No Reference'),
    ('begin_baud', 'Begin of the first baud'),
    ('first_baud', 'Middle of the first baud'),
    ('sub_baud', 'Middle of the sub-baud')
                 )

DAT_CMDS = {
        # Pulse Design commands
        'DISABLE' : 0, # Disables pulse generation
        'ENABLE' : 24, # Enables pulse generation
        'DELAY_START' : 40, # Write delay status to memory
        'FLIP_START' : 48, # Write flip status to memory
        'SAMPLING_PERIOD' : 64, # Establish Sampling Period
        'TX_ONE' : 72, # Output '0' in line TX
        'TX_ZERO' : 88, # Output '0' in line TX
        'SW_ONE' : 104, # Output '0' in line SW
        'SW_ZERO' : 112, # Output '1' in line SW
        'RESTART': 120, # Restarts CR8 Firmware
        'CONTINUE' : 253, # Function Unknown
        # Commands available to new controllers
        # In Pulse Design Executable, the clock divisor code is written as 12 at the start, but it should be written as code 22(below) just before the final enable.
        'CLOCK_DIVISOR_INIT' : 12, # Specifies Clock Divisor. Legacy command, ignored in the actual .dat conversion
        'CLOCK_DIVISOR_LAST' : 22, # Specifies Clock Divisor (default 60 if not included) syntax: 255,22 254,N-1.
        'CLOCK_DIVIDER' : 8,
            }


class RCConfiguration(Configuration):

    ipp = models.FloatField(verbose_name='IPP [Km]', validators=[MinValueValidator(1), MaxValueValidator(9000)], default=300)
    ntx = models.PositiveIntegerField(verbose_name='Number of TX', validators=[MinValueValidator(1), MaxValueValidator(400)], default=1)
    clock_in = models.FloatField(verbose_name='Clock in [MHz]', validators=[MinValueValidator(1), MaxValueValidator(80)], default=1)
    clock_divider = models.PositiveIntegerField(verbose_name='Clock divider', validators=[MinValueValidator(1), MaxValueValidator(256)], default=1)
    clock = models.FloatField(verbose_name='Clock Master [MHz]', blank=True, default=1)
    time_before = models.PositiveIntegerField(verbose_name='Time before [&mu;S]', default=12)
    time_after = models.PositiveIntegerField(verbose_name='Time after [&mu;S]', default=1)
    sync = models.PositiveIntegerField(verbose_name='Synchro delay', default=0)
    sampling_reference = models.CharField(verbose_name='Sampling Reference', choices=SAMPLING_REFS, default='none', max_length=40)
    control_tx = models.BooleanField(verbose_name='Control Switch TX', default=False)
    control_sw = models.BooleanField(verbose_name='Control Switch SW', default=False)
    total_units = models.PositiveIntegerField(default=0)
    mix = models.BooleanField(default=False)

    class Meta:
        db_table = 'rc_configurations'

    def get_absolute_url_plot(self):
        return reverse('url_plot_rc_pulses', args=[str(self.id)])

    def get_absolute_url_import(self):
        return reverse('url_import_rc_conf', args=[str(self.id)])

    @property
    def ipp_unit(self):

        return '{} ({})'.format(self.ipp, int(self.ipp*self.km2unit))

    @property
    def us2unit(self):

        return self.clock_in/self.clock_divider

    @property
    def km2unit(self):

        return 20./3*(self.clock_in/self.clock_divider)

    def clone(self, **kwargs):

        lines = self.get_lines()
        self.pk = None
        self.id = None
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        self.save()

        for line in lines:
            line.clone(rc_configuration=self)

        return self

    def get_lines(self, **kwargs):
        '''
        Retrieve configuration lines
        '''

        return RCLine.objects.filter(rc_configuration=self.pk, **kwargs)


    def clean_lines(self):
        '''
        '''

        empty_line = RCLineType.objects.get(name='none')

        for line in self.get_lines():
            line.line_type = empty_line
            line.params = '{}'
            line.save()

    def parms_to_dict(self):
        '''
        '''

        ignored = ('parameters', 'type', 'polymorphic_ctype', 'configuration_ptr',
                   'created_date', 'programmed_date')

        data = {}
        for field in self._meta.fields:
            if field.name in ignored:
                continue
            data[field.name] = '{}'.format(field.value_from_object(self))

        data['device_id'] = data.pop('device')
        data['lines'] = []

        for line in self.get_lines():
            line_data = json.loads(line.params)
            if 'TX_ref' in line_data and line_data['TX_ref'] not in (0, '0'):
                line_data['TX_ref'] = RCLine.objects.get(pk=line_data['TX_ref']).get_name()
            if 'code' in line_data:
                line_data['code'] = RCLineCode.objects.get(pk=line_data['code']).name
            line_data['type'] = line.line_type.name
            line_data['name'] = line.get_name()
            data['lines'].append(line_data)

        data['delays'] = self.get_delays()
        data['pulses'] = self.get_pulses()

        return data

    def dict_to_parms(self, data):
        '''
        '''

        self.name = data['name']
        self.ipp = float(data['ipp'])
        self.ntx = int(data['ntx'])
        self.clock_in = float(data['clock_in'])
        self.clock_divider = int(data['clock_divider'])
        self.clock = float(data['clock'])
        self.time_before = data['time_before']
        self.time_after = data['time_after']
        self.sync = data['sync']
        self.sampling_reference = data['sampling_reference']
        self.total_units = self.ipp*self.ntx*self.km2unit
        self.save()
        self.clean_lines()

        lines = []
        positions = {'tx':0, 'tr':0}

        for i, line_data in enumerate(data['lines']):
            name = line_data.pop('name', '')
            line_type = RCLineType.objects.get(name=line_data.pop('type'))
            if line_type.name=='codes':
                code = RCLineCode.objects.get(name=line_data['code'])
                line_data['code'] = code.pk
            line = RCLine.objects.filter(rc_configuration=self, channel=i)
            if line:
                line = line[0]
                line.line_type = line_type
                line.params = json.dumps(line_data)
            else:
                line = RCLine(rc_configuration=self, line_type=line_type,
                              params=json.dumps(line_data),
                              channel=i)

            if line_type.name=='tx':
                line.position = positions['tx']
                positions['tx'] += 1

            if line_type.name=='tr':
                line.position = positions['tr']
                positions['tr'] += 1

            line.save()
            lines.append(line)

        for line, line_data in zip(lines, data['lines']):
            if 'TX_ref' in line_data:
                params = json.loads(line.params)
                if line_data['TX_ref'] in (0, '0'):
                    params['TX_ref'] = '0'
                else:
                    params['TX_ref'] = [l.pk for l in lines if l.line_type.name=='tx' and line_data['TX_ref'] in l.get_name()][0]
                line.params = json.dumps(params)
                line.save()


    def get_delays(self):

        pulses = [line.pulses_as_points() for line in self.get_lines()]
        points = [tup for tups in pulses for tup in tups]
        points = set([x for tup in points for x in tup])
        points = list(points)
        points.sort()

        if points[0]!=0:
            points.insert(0, 0)

        return [points[i+1]-points[i] for i in range(len(points)-1)]


    def get_pulses(self, binary=True):

        pulses = [line.pulses_as_points() for line in self.get_lines()]
        points = [tup for tups in pulses for tup in tups]
        points = set([x for tup in points for x in tup])
        points = list(points)
        points.sort()

        line_points = [line.pulses_as_points() for line in self.get_lines()]
        #line_points = [[(x, x+y) for x,y in tups] for tups in line_points]
        line_points = [[t for x in tups for t in x] for tups in line_points]
        states = [[1 if x in tups else 0 for tups in line_points] for x in points]

        if binary:
            states.reverse()
            states = [int(''.join([str(x) for x in flips]), 2) for flips in states]

        return states[:-1]

    def add_cmd(self, cmd):

        if cmd in DAT_CMDS:
            return (255, DAT_CMDS[cmd])

    def add_data(self, value):

        return (254, value-1)
    
    def parms_to_binary(self, dat=True):
        '''
        Create "dat" stream to be send to CR
        '''

        data = bytearray()
        # create header
        data.extend(self.add_cmd('DISABLE'))
        data.extend(self.add_cmd('CONTINUE'))
        data.extend(self.add_cmd('RESTART'))

        if self.control_sw:
            data.extend(self.add_cmd('SW_ONE'))
        else:
            data.extend(self.add_cmd('SW_ZERO'))

        if self.control_tx:
            data.extend(self.add_cmd('TX_ONE'))
        else:
            data.extend(self.add_cmd('TX_ZERO'))

        # write divider
        data.extend(self.add_cmd('CLOCK_DIVIDER'))
        data.extend(self.add_data(self.clock_divider))

        # write delays
        data.extend(self.add_cmd('DELAY_START'))
        # first delay is always zero
        data.extend(self.add_data(1))

        delays = self.get_delays()

        for delay in delays:
            while delay>252:
                data.extend(self.add_data(253))
                delay -= 253
            data.extend(self.add_data(int(delay)))

        # write flips
        data.extend(self.add_cmd('FLIP_START'))

        states = self.get_pulses(binary=False)

        for flips, delay in zip(states, delays):
            flips.reverse()
            flip = int(''.join([str(x) for x in flips]), 2)
            data.extend(self.add_data(flip+1))
            while delay>252:
                data.extend(self.add_data(1))
                delay -= 253

        # write sampling period
        data.extend(self.add_cmd('SAMPLING_PERIOD'))
        wins = self.get_lines(line_type__name='windows')
        if wins:
            win_params = json.loads(wins[0].params)['params']
            if win_params:
                dh = int(win_params[0]['resolution']*self.km2unit)
            else:
                dh = 1
        else:
            dh = 1
        data.extend(self.add_data(dh))

        # write enable
        data.extend(self.add_cmd('ENABLE'))        

        if not dat:
            return data

        return '\n'.join(['{}'.format(x) for x in data])


    def update_from_file(self, filename):
        '''
        Update instance from file
        '''

        f = RCFile(filename)
        self.dict_to_parms(f.data)
        self.update_pulses()

    def update_pulses(self):

        for line in self.get_lines():
            line.update_pulses()

    def plot_pulses2(self, km=False):

        import matplotlib.pyplot as plt
        from bokeh.resources import CDN
        from bokeh.embed import components
        from bokeh.mpl import to_bokeh
        from bokeh.models.tools import WheelZoomTool, ResetTool, PanTool, HoverTool, SaveTool

        lines = self.get_lines()

        N = len(lines)
        npoints = self.total_units/self.km2unit if km else self.total_units
        fig = plt.figure(figsize=(12, 2+N*0.5))
        ax = fig.add_subplot(111)
        labels = ['IPP']

        for i, line in enumerate(lines):
            labels.append(line.get_name(channel=True))
            l = ax.plot((0, npoints),(N-i-1, N-i-1))
            points = [(tup[0], tup[1]-tup[0]) for tup in line.pulses_as_points(km=km) if tup!=(0,0)]
            ax.broken_barh(points, (N-i-1, 0.5),
                           edgecolor=l[0].get_color(), facecolor='none')

        n = 0
        f = ((self.ntx+50)/100)*5 if ((self.ntx+50)/100)*10>0 else 2
        for x in np.arange(0, npoints, self.ipp if km else self.ipp*self.km2unit):
            if n%f==0:
                ax.text(x, N, '%s' % n, size=10)
            n += 1


        labels.reverse()
        ax.set_yticks(range(len(labels)))
        ax.set_yticklabels(labels)
        ax.set_xlabel = 'Units'
        plot = to_bokeh(fig, use_pandas=False)        
        plot.tools = [PanTool(dimensions=['width']), WheelZoomTool(dimensions=['width']), ResetTool(), SaveTool()]
        plot.toolbar_location="above"

        return components(plot, CDN)

    def plot_pulses(self, km=False):

        from bokeh.plotting import figure
        from bokeh.resources import CDN
        from bokeh.embed import components
        from bokeh.models import FixedTicker, PrintfTickFormatter
        from bokeh.models.tools import WheelZoomTool, ResetTool, PanTool, HoverTool, SaveTool
        from bokeh.models.sources import ColumnDataSource

        lines = self.get_lines().reverse()
        
        N = len(lines)
        npoints = self.total_units/self.km2unit if km else self.total_units
        ipp = self.ipp if km else self.ipp*self.km2unit
        
        hover = HoverTool(tooltips=[("Line", "@name"),
                                    ("IPP", "@ipp"),
                                    ("X", "@left")])
        
        tools = [PanTool(dimensions=['width']), 
                 WheelZoomTool(dimensions=['width']), 
                 hover, SaveTool()]
        
        plot = figure(width=1000, 
                      height=40+N*50, 
                      y_range = (0, N),
                      tools=tools, 
                      toolbar_location='above',
                      toolbar_sticky=False,)            
                
        plot.xaxis.axis_label = 'Km' if km else 'Units'
        plot.xaxis[0].formatter = PrintfTickFormatter(format='%d')
        plot.yaxis.axis_label = 'Pulses'        
        plot.yaxis[0].ticker=FixedTicker(ticks=list(range(N)))
        plot.yaxis[0].formatter = PrintfTickFormatter(format='Line %d')

        for i, line in enumerate(lines):            
            
            points = [tup for tup in line.pulses_as_points(km=km) if tup!=(0,0)]
            
            source = ColumnDataSource(data = dict(
                                                  bottom = [i for tup in points],
                                                  top = [i+0.5 for tup in points],
                                                  left = [tup[0] for tup in points],
                                                  right = [tup[1] for tup in points],
                                                  ipp = [int(tup[0]/ipp) for tup in points],
                                                  name = [line.get_name() for tup in points]
                                                  ))
            
            plot.quad(
                     bottom = 'bottom',
                     top = 'top',
                     left = 'left',
                     right = 'right',
                     source = source,
                     fill_alpha = 0,
                     #line_color = 'blue',
                     )
            
            plot.line([0, npoints], [i, i])#, color='blue')

        return components(plot, CDN)

    def status_device(self):

        try:
            self.device.status = 0
            req = requests.get(self.device.url('status'))
            payload = req.json()
            if payload['status']=='ok':
                self.device.status = 2
            else:
                self.device.status = 1                
                self.device.save()
                self.message = payload['status']
                return False
        except Exception as e:
            if 'No route to host' not in str(e):
                self.device.status = 4
            self.device.save()
            self.message = str(e)
            return False
            
        self.device.save()        
        return True            

    def reset_device(self):
                
        try:
            req = requests.post(self.device.url('reset'))
            payload = req.json()       
            if payload['reset']=='ok':
                self.message = 'RC restarted'
            else:
                self.message = 'RC restart not ok'                
                self.device.status = 4
                self.device.save()
        except Exception as e:
            self.message = str(e)
            return False
            
        return True
        
    def stop_device(self):

        try:
            req = requests.post(self.device.url('stop'))
            payload = req.json()          
            if payload['stop']=='ok':
                self.device.status = 2
                self.device.save()
                self.message = 'RC stopped'
            else:
                self.message = 'RC stop not ok'
                self.device.status = 4
                self.device.save()
                return False
        except Exception as e:
            if 'No route to host' not in str(e):
                self.device.status = 4
            else:
                self.device.status = 0
            self.message = str(e)            
            self.device.save()
            return False            
        
        return True

    def start_device(self):

        try:
            req = requests.post(self.device.url('start'))
            payload = req.json()
            if payload['start']=='ok':
                self.device.status = 3
                self.device.save()
                self.message = 'RC running'
            else:
                self.message = 'RC start not ok'
                return False
        except Exception as e:
            if 'No route to host' not in str(e):
                self.device.status = 4
            else:
                self.device.status = 0
            self.message = str(e)            
            self.device.save()
            return False
                    
        return True

    def write_device(self):
        
        values = zip(self.get_pulses(), 
                     [x-1 for x in self.get_delays()])
        payload = ''
        
        for tup in values:
            vals = pack('<HH', *tup)
            payload += '\x05'+vals[0]+'\x04'+vals[1]+'\x05'+vals[2]+'\x05'+vals[3]        
        
        try:
            ## reset                        
            if not self.reset_device():
                return False
            ## stop
            if not self.stop_device():
                return False
            ## write clock divider
            req = requests.post(self.device.url('divisor'), 
                                {'divisor': '{:d}'.format(self.clock_divider-1)})
            payload = req.json()
            if payload['divisor']=='ok':
                self.message = 'Error configuring RC clock divider'
                return False
            ## write pulses & delays
            req = requests.post(self.device.url('write'), data=b64encode(payload))
            payload = req.json()            
            if payload['write']=='ok':
                self.device.status = 2
                self.device.save()
                self.message = 'RC configured'
            else:
                self.device.status = 4
                self.device.save()
                self.message = 'RC write not ok'
                return False
        
        except Exception as e:
            if 'No route to host' not in str(e):
                self.device.status = 4
            else:
                self.device.status = 0
            self.message = str(e)            
            self.device.save()
            return False
                    
        return True


class RCLineCode(models.Model):

    name = models.CharField(max_length=40)
    bits_per_code = models.PositiveIntegerField(default=0)
    number_of_codes = models.PositiveIntegerField(default=0)
    codes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'rc_line_codes'
        ordering = ('name',)

    def __str__(self):
        return u'%s' % self.name


class RCLineType(models.Model):

    name = models.CharField(choices=LINE_TYPES, max_length=40)
    description = models.TextField(blank=True, null=True)
    params = models.TextField(default='[]')

    class Meta:
        db_table = 'rc_line_types'

    def __str__(self):
        return u'%s - %s' % (self.name.upper(), self.get_name_display())


class RCLine(models.Model):

    rc_configuration = models.ForeignKey(RCConfiguration, on_delete=models.CASCADE)
    line_type = models.ForeignKey(RCLineType)
    channel = models.PositiveIntegerField(default=0)
    position = models.PositiveIntegerField(default=0)
    params = models.TextField(default='{}')
    pulses = models.TextField(default='')

    class Meta:
        db_table = 'rc_lines'
        ordering = ['channel']

    def __str__(self):
        if self.rc_configuration:
            return u'%s - %s' % (self.rc_configuration, self.get_name())

    def clone(self, **kwargs):

        self.pk = None

        for attr, value in kwargs.items():
            setattr(self, attr, value)

        self.save()

        return self

    def get_name(self, channel=False):

        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        s = ''

        if self.line_type.name in ('tx',):
            s = chars[self.position]
        elif self.line_type.name in ('codes', 'windows', 'tr'):
            if 'TX_ref' in json.loads(self.params):
                pk = json.loads(self.params)['TX_ref']
                if pk in (0, '0'):
                    s = ','.join(chars[l.position] for l in self.rc_configuration.get_lines(line_type__name='tx'))
                else:
                    ref = RCLine.objects.get(pk=pk)
                    s = chars[ref.position]
                s = '({})'.format(s)

        s = '{}{}'.format(self.line_type.name.upper(), s)

        if channel:
            return '{} {}'.format(s, self.channel)
        else:
            return s

    def get_lines(self, **kwargs):

        return RCLine.objects.filter(rc_configuration=self.rc_configuration, **kwargs)

    def pulses_as_array(self):

        y = np.zeros(self.rc_configuration.total_units)

        for tup in ast.literal_eval(self.pulses):
            y[tup[0]:tup[1]] = 1

        return y.astype(np.int8)

    def pulses_as_points(self, km=False):

        if km:
            unit2km = 1/self.rc_configuration.km2unit
            return [(tup[0]*unit2km, tup[1]*unit2km) for tup in ast.literal_eval(self.pulses)]
        else:
            return ast.literal_eval(self.pulses)

    def get_win_ref(self, params, tx_id, km2unit):

        ref = self.rc_configuration.sampling_reference
        codes = [line for line in self.get_lines(line_type__name='codes') if int(json.loads(line.params)['TX_ref'])==int(tx_id)]

        if codes:
            tx_width = float(json.loads(RCLine.objects.get(pk=tx_id).params)['pulse_width'])*km2unit/len(json.loads(codes[0].params)['codes'][0])
        else:
            tx_width = float(json.loads(RCLine.objects.get(pk=tx_id).params)['pulse_width'])*km2unit

        if ref=='first_baud':
            return int(1 + (tx_width + 1)/2 + params['first_height']*km2unit - params['resolution']*km2unit)
        elif ref=='sub_baud':
            return int(1 + params['first_height']*km2unit - params['resolution']*km2unit/2)
        else:
            return 0

    def update_pulses(self):
        '''
        Update pulses field
        '''

        km2unit = self.rc_configuration.km2unit
        us2unit = self.rc_configuration.us2unit
        ipp = self.rc_configuration.ipp
        ntx = int(self.rc_configuration.ntx)
        ipp_u = int(ipp*km2unit)
        total = ipp_u*ntx if self.rc_configuration.total_units==0 else self.rc_configuration.total_units
        y = []

        if self.line_type.name=='tr':
            tr_params = json.loads(self.params)

            if tr_params['TX_ref'] in ('0', 0):
                txs = self.get_lines(line_type__name='tx')
            else:
                txs = RCLine.objects.filter(pk=tr_params['TX_ref'])

            for tx in txs:
                params = json.loads(tx.params)

                if float(params['pulse_width'])==0:
                    continue
                delays = [float(d)*km2unit for d in params['delays'].split(',') if d]
                width = float(params['pulse_width'])*km2unit+int(self.rc_configuration.time_before*us2unit)
                before = 0
                after = int(self.rc_configuration.time_after*us2unit)

                y_tx = self.points(ntx, ipp_u, width,
                                   delay=delays,
                                   before=before,
                                   after=after,
                                   sync=self.rc_configuration.sync)

                ranges = params['range'].split(',')

                if len(ranges)>0 and ranges[0]!='0':
                    y_tx = self.mask_ranges(y_tx, ranges)

                tr_ranges = tr_params['range'].split(',')

                if len(tr_ranges)>0 and tr_ranges[0]!='0':
                    y_tx = self.mask_ranges(y_tx, tr_ranges)

                y.extend(y_tx)

            self.pulses = str(y)
            y = self.array_to_points(self.pulses_as_array())

        elif self.line_type.name=='tx':
            params = json.loads(self.params)
            delays = [float(d)*km2unit for d in params['delays'].split(',') if d]
            width = float(params['pulse_width'])*km2unit

            if width>0:
                before = int(self.rc_configuration.time_before*us2unit)
                after = 0

                y = self.points(ntx, ipp_u, width,
                                delay=delays,
                                before=before,
                                after=after,
                                sync=self.rc_configuration.sync)

                ranges = params['range'].split(',')

                if len(ranges)>0 and ranges[0]!='0':
                    y = self.mask_ranges(y, ranges)

        elif self.line_type.name=='flip':
            n = float(json.loads(self.params)['number_of_flips'])
            width = n*ipp*km2unit
            y = self.points(int((ntx+1)/(2*n)), ipp_u*n*2, width)

        elif self.line_type.name=='codes':
            params = json.loads(self.params)
            tx = RCLine.objects.get(pk=params['TX_ref'])
            tx_params = json.loads(tx.params)
            delays = [float(d)*km2unit for d in tx_params['delays'].split(',') if d]
            f = int(float(tx_params['pulse_width'])*km2unit/len(params['codes'][0]))
            codes = [(np.fromstring(''.join([s*f for s in code]), dtype=np.uint8)-48).astype(np.int8) for code in params['codes']]
            codes = [self.array_to_points(code) for code in codes]
            n = len(codes)

            for i, tup in enumerate(tx.pulses_as_points()):
                code = codes[i%n]
                y.extend([(c[0]+tup[0], c[1]+tup[0]) for c in code])

            ranges = tx_params['range'].split(',')
            if len(ranges)>0 and ranges[0]!='0':
                y = self.mask_ranges(y, ranges)

        elif self.line_type.name=='sync':
            params = json.loads(self.params)
            n = ipp_u*ntx
            if params['invert'] in ('1', 1):
                y = [(n-1, n)]
            else:
                y = [(0, 1)]

        elif self.line_type.name=='prog_pulses':
            params = json.loads(self.params)
            if int(params['periodic'])==0:
                nntx = 1
                nipp = ipp_u*ntx
            else:
                nntx = ntx
                nipp = ipp_u

            if 'params' in params and len(params['params'])>0:
                for p in params['params']:
                    y_pp = self.points(nntx, nipp,
                                       p['end']-p['begin'],
                                       before=p['begin'])

                    y.extend(y_pp)

        elif self.line_type.name=='windows':
            params = json.loads(self.params)

            if 'params' in params and len(params['params'])>0:
                tr_params = json.loads(self.get_lines(line_type__name='tr')[0].params)
                tr_ranges = tr_params['range'].split(',')
                for p in params['params']:
                    y_win = self.points(ntx, ipp_u,
                                        p['resolution']*p['number_of_samples']*km2unit,
                                        before=int(self.rc_configuration.time_before*us2unit)+self.get_win_ref(p, params['TX_ref'], km2unit),
                                        sync=self.rc_configuration.sync)

                    if len(tr_ranges)>0 and tr_ranges[0]!='0':
                        y_win = self.mask_ranges(y_win, tr_ranges)

                    y.extend(y_win)

        elif self.line_type.name=='mix':
            values = self.rc_configuration.parameters.split('-')
            confs = [RCConfiguration.objects.get(pk=value.split('|')[0]) for value in values]
            modes = [value.split('|')[1] for value in values]
            ops = [value.split('|')[2] for value in values]
            delays = [value.split('|')[3] for value in values]
            masks = [value.split('|')[4] for value in values]
            mask = list('{:8b}'.format(int(masks[0])))
            mask.reverse()
            if mask[self.channel] in ('0', '', ' '):
                y = np.zeros(confs[0].total_units, dtype=np.int8)
            else:
                y = confs[0].get_lines(channel=self.channel)[0].pulses_as_array()

            for i in range(1, len(values)):
                mask = list('{:8b}'.format(int(masks[i])))
                mask.reverse()

                if mask[self.channel] in ('0', '', ' '):
                    continue
                Y = confs[i].get_lines(channel=self.channel)[0].pulses_as_array()
                delay = float(delays[i])*km2unit

                if modes[i]=='P':
                    if delay>0:
                        if delay<self.rc_configuration.ipp*km2unit and len(Y)==len(y):
                            y_temp = np.empty_like(Y)
                            y_temp[:delay] = 0
                            y_temp[delay:] = Y[:-delay]
                        elif delay+len(Y)>len(y):
                            y_new = np.zeros(delay+len(Y), dtype=np.int8)
                            y_new[:len(y)] = y
                            y = y_new
                            y_temp = np.zeros(delay+len(Y), dtype=np.int8)
                            y_temp[-len(Y):] = Y
                        elif delay+len(Y)==len(y):
                            y_temp = np.zeros(delay+len(Y))
                            y_temp[-len(Y):] = Y
                        elif delay+len(Y)<len(y):
                            y_temp = np.zeros(len(y), dtype=np.int8)
                            y_temp[delay:delay+len(Y)] = Y

                    if ops[i]=='OR':
                        y = y | y_temp
                    elif ops[i]=='XOR':
                        y = y ^ y_temp
                    elif ops[i]=='AND':
                        y = y & y_temp
                    elif ops[i]=='NAND':
                        y = y & ~y_temp
                else:
                    y = np.concatenate([y, Y])

            total = len(y)
            y = self.array_to_points(y)

        else:
            y = []

        if self.rc_configuration.total_units != total:
            self.rc_configuration.total_units = total
            self.rc_configuration.save()

        self.pulses = str(y)
        self.save()

    @staticmethod
    def array_to_points(X):

        d = X[1:]-X[:-1]

        up = np.where(d==1)[0]
        if X[0]==1:
            up = np.concatenate((np.array([-1]), up))
        up += 1

        dw = np.where(d==-1)[0]
        if X[-1]==1:
            dw = np.concatenate((dw, np.array([len(X)-1])))
        dw += 1

        return [(tup[0], tup[1]) for tup in zip(up, dw)]

    @staticmethod
    def mask_ranges(Y, ranges):

        y = [(0, 0) for __ in Y]

        for index in ranges:
            if '-' in index:
                args = [int(a) for a in index.split('-')]
                y[args[0]-1:args[1]] = Y[args[0]-1:args[1]]
            else:
                y[int(index-1)] = Y[int(index-1)]

        return y

    @staticmethod
    def points(ntx, ipp, width, delay=[0], before=0, after=0, sync=0):

        delays = len(delay)

        Y = [(int(ipp*x+before+delay[x%delays]+sync), int(ipp*x+width+before+delay[x%delays]+after+sync)) for x in range(ntx)]

        return Y
