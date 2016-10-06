from django.db import models
from apps.main.models import Configuration
from django.core.urlresolvers import reverse
# Create your models here.

import ast
import socket
import json
import requests
import struct
import sys, time

import multiprocessing


antenna_default = json.dumps({
                    "antenna_up": [[0.0,0.0,0.0,0.0,0.5,0.5,0.5,0.5],
                                    [0.0,0.0,0.0,0.0,0.5,0.5,0.5,0.5],
                                    [0.0,0.0,0.0,0.0,0.5,0.5,0.5,0.5],
                                    [0.0,0.0,0.0,0.0,0.5,0.5,0.5,0.5],
                                    [0.5,0.5,0.5,0.5,1.0,1.0,1.0,1.0],
                                    [0.5,0.5,0.5,0.5,1.0,1.0,1.0,1.0],
                                    [0.5,0.5,0.5,0.5,1.0,1.0,1.0,1.0],
                                    [0.5,0.5,0.5,0.5,1.0,1.0,1.0,1.0]
                                    ]
                                   ,
                    "antenna_down": [[0.0,0.0,0.0,0.0,0.5,0.5,0.5,0.5],
                                    [0.0,0.0,0.0,0.0,0.5,0.5,0.5,0.5],
                                    [0.0,0.0,0.0,0.0,0.5,0.5,0.5,0.5],
                                    [0.0,0.0,0.0,0.0,0.5,0.5,0.5,0.5],
                                    [0.5,0.5,0.5,0.5,3.0,3.0,3.0,3.0],
                                    [0.5,0.5,0.5,0.5,3.0,3.0,3.0,3.0],
                                    [0.5,0.5,0.5,0.5,3.0,3.0,3.0,3.0],
                                    [0.5,0.5,0.5,0.5,3.0,3.0,3.0,3.0]],
                })


tx_default = json.dumps({
                "up": [[1,1,1,1,0,0,0,0],
                       [1,1,1,1,0,0,0,0],
                       [1,1,1,1,0,0,0,0],
                       [1,1,1,1,0,0,0,0],
                       [0,0,0,0,1,1,1,1],
                       [0,0,0,0,1,1,1,1],
                       [0,0,0,0,1,1,1,1],
                       [0,0,0,0,1,1,1,1]],

              "down": [[1,1,1,1,0,0,0,0],
                       [1,1,1,1,0,0,0,0],
                       [1,1,1,1,0,0,0,0],
                       [1,1,1,1,0,0,0,0],
                       [0,0,0,0,1,1,1,1],
                       [0,0,0,0,1,1,1,1],
                       [0,0,0,0,1,1,1,1],
                       [0,0,0,0,1,1,1,1]],
             })

rx_default = json.dumps({
                "up": [[1,1,1,1,0,0,0,0],
                       [1,1,1,1,0,0,0,0],
                       [1,1,1,1,0,0,0,0],
                       [1,1,1,1,0,0,0,0],
                       [0,0,0,0,1,1,1,1],
                       [0,0,0,0,1,1,1,1],
                       [0,0,0,0,1,1,1,1],
                       [0,0,0,0,1,1,1,1]],

              "down": [[1,1,1,1,0,0,0,0],
                       [1,1,1,1,0,0,0,0],
                       [1,1,1,1,0,0,0,0],
                       [1,1,1,1,0,0,0,0],
                       [0,0,0,0,1,1,1,1],
                       [0,0,0,0,1,1,1,1],
                       [0,0,0,0,1,1,1,1],
                       [0,0,0,0,1,1,1,1]],
             })

conf_default = {}
status_default = {}
for i in range(1,65):
    conf_default[str(i)] = ""
    status_default[str(i)] = 0

ues_default = json.dumps({
                "up": [0.533333,0.00000,1.06667,0.00000],
                "down": [0.533333,0.00000,1.06667,0.00000]
            })

onlyrx_default = json.dumps({
                    "up": False,
                    "down": False
                })

def up_convertion(cadena):
    valores = []
    for c in cadena:
        if c == 1.0: valores=valores+['000']
        if c == 2.0: valores=valores+['001']
        if c == 3.0: valores=valores+['010']
        if c == 0.0: valores=valores+['011']
        if c == 0.5: valores=valores+['100']
        if c == 1.5: valores=valores+['101']
        if c == 2.5: valores=valores+['110']
        if c == 3.5: valores=valores+['111']

    return valores

def up_conv_bits(value):

    if value == 1.0: bits="000"
    if value == 2.0: bits="001"
    if value == 3.0: bits="010"
    if value == 0.0: bits="011"
    if value == 0.5: bits="100"
    if value == 1.5: bits="101"
    if value == 2.5: bits="110"
    if value == 3.5: bits="111"

    return bits

def down_convertion(cadena):
    valores = []
    for c in cadena:
        if c == 1.0: valores=valores+['000']
        if c == 2.0: valores=valores+['001']
        if c == 3.0: valores=valores+['010']
        if c == 0.0: valores=valores+['011']
        if c == 0.5: valores=valores+['100']
        if c == 1.5: valores=valores+['101']
        if c == 2.5: valores=valores+['110']
        if c == 3.5: valores=valores+['111']

    return valores

def down_conv_bits(value):

    if value == 1.0: bits="000"
    if value == 2.0: bits="001"
    if value == 3.0: bits="010"
    if value == 0.0: bits="011"
    if value == 0.5: bits="100"
    if value == 1.5: bits="101"
    if value == 2.5: bits="110"
    if value == 3.5: bits="111"

    return bits

def ip2position(module_number):
    j=0
    i=0
    for x in range(0,module_number-1):
        j=j+1
        if j==8:
            i=i+1
            j=0

    pos = [i,j]
    return pos


def fromBinary2Char(binary_string):
    number = int(binary_string, 2)
    #Plus 33 to avoid more than 1 characters values such as: '\x01'-'\x1f'
    number = number + 33
    char = chr(number)
    return char

def fromChar2Binary(char):
    number = ord(char) - 33
    #Minus 33 to get the real value
    bits = bin(number)[2:]
    #To ensure we have a string with 6bits
    if len(bits) < 6:
        bits = bits.zfill(6)
    return bits

OPERATION_MODES = (
                 (0, 'Manual'),
                 (1, 'Automatic'),
             )


class ABSConfiguration(Configuration):
    active_beam     = models.CharField(verbose_name='Active Beam', max_length=20000, default="{}")
    module_status   = models.CharField(verbose_name='Module Status', max_length=10000, default=json.dumps(status_default))
    operation_mode  = models.PositiveSmallIntegerField(verbose_name='Operation Mode', choices=OPERATION_MODES, default = 0)
    operation_value = models.FloatField(verbose_name='Periodic (seconds)', default="10", null=True, blank=True)

    class Meta:
        db_table = 'abs_configurations'

    def get_absolute_url_plot(self):
        return reverse('url_plot_abs_patterns', args=[str(self.id)])


    def parms_to_dict(self):

        parameters = {}

        parameters['device_id'] = self.device.id
        parameters['name']      = self.name
        parameters['beams']     = {}

        beams = ABSBeam.objects.filter(abs_conf=self)
        b=1
        for beam in beams:
            #absbeam = ABSBeam.objects.get(pk=beams[beam])
            parameters['beams']['beam'+str(b)] = beam.parms_to_dict()#absbeam.parms_to_dict()
            b+=1

        return parameters

    def dict_to_parms(self, parameters):

        self.name = parameters['name']

        absbeams  = ABSBeam.objects.filter(abs_conf=self)
        beams     = parameters['beams']

        if absbeams:
            beams_number    = len(beams)
            absbeams_number = len(absbeams)
            if beams_number==absbeams_number:
                i = 1
                for absbeam in absbeams:
                    absbeam.dict_to_parms(beams['beam'+str(i)])
                    i = i+1
            elif beams_number > absbeams_number:
                i = 1
                for absbeam in absbeams:
                    absbeam.dict_to_parms(beams['beam'+str(i)])
                    i=i+1
                for x in range(i,beams_number+1):
                    new_beam = ABSBeam(
                               name     =beams['beam'+str(i)]['name'],
                               antenna  =json.dumps(beams['beam'+str(i)]['antenna']),
                               abs_conf = self,
                               tx       =json.dumps(beams['beam'+str(i)]['tx']),
                               rx       =json.dumps(beams['beam'+str(i)]['rx']),
                               ues      =json.dumps(beams['beam'+str(i)]['ues']),
                               only_rx  =json.dumps(beams['beam'+str(i)]['only_rx'])
                               )
                    new_beam.save()
                    i=i+1
            else: #beams_number < absbeams_number:
                i = 1
                for absbeam in absbeams:
                    if i <= beams_number:
                        absbeam.dict_to_parms(beams['beam'+str(i)])
                        i=i+1
                    else:
                        absbeam.delete()
        else:
            for beam in beams:
                new_beam = ABSBeam(
                           name     =beams[beam]['name'],
                           antenna  =json.dumps(beams[beam]['antenna']),
                           abs_conf = self,
                           tx       =json.dumps(beams[beam]['tx']),
                           rx       =json.dumps(beams[beam]['rx']),
                           ues      =json.dumps(beams[beam]['ues']),
                           only_rx  =json.dumps(beams[beam]['only_rx'])
                           )
                new_beam.save()



    def update_from_file(self, parameters):

        self.dict_to_parms(parameters)
        self.save()


    def get_beams(self, **kwargs):
        '''
        This function returns ABS Configuration beams
        '''
        return ABSBeam.objects.filter(abs_conf=self.pk, **kwargs)

    def clone(self, **kwargs):

        beams = self.get_beams()
        self.pk = None
        self.id = None
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        self.save()

        for beam in beams:
            beam.clone(abs_conf=self)

        return self


    def module_conf(self, module_num, beams):
        """
        This function creates beam configurations for one abs module.
        """
        ip_address  = self.device.ip_address
        ip_address  = ip_address.split('.')
        module_seq  = (ip_address[0],ip_address[1],ip_address[2])
        dot         = '.'
        module_ip   = dot.join(module_seq)+'.'+str(module_num)
        module_port = self.device.port_address
        write_route = 'http://'+module_ip+':'+str(module_port)+'/write'

        header = 'JROABSCeCnModCnMod01000108SNDFexperimento1.ab1'
        module = 'ABS_'+str(module_num)
        bs  = '' #{}
        i=1

        for beam in beams:
            #bs[i] = fromBinary2Char(beam.module_6bits(module_num))
            bs = bs + fromBinary2Char(beam.module_6bits(module_num))
            i=i+1

        beams = bs

        parameters = {}
        #parameters['header'] = header
        #parameters['module'] = module
        parameters['beams']  = beams #json.dumps(beams)
        #print beams
        #print parameters['beams']
        print parameters
        answer = ''

        try:
            #r_write = requests.post(write_route, parameters, timeout=0.5)
            r_write = requests.post(write_route, json = parameters, timeout=0.5)
            answer  = r_write.json()
            self.message = answer['message']
        except:
            self.message = "Could not write ABS parameters"
            return 0
        return 1



    def write_device(self):
        """
        This function sends the beams list to every abs module.
        It needs 'module_conf' function
        """

        beams = ABSBeam.objects.filter(abs_conf=self)

        #-------------Write each abs module-----------
        if beams:
            beams_status = ast.literal_eval(self.module_status)
            for i in range(61,64): #(62,65)
                try:
                    answer = self.module_conf(i, beams)
                    beams_status[str(i)] = 1
                    self.module_status = json.dumps(beams_status)
                    self.save()

                except:
                    beams_status[str(i)] = 0
                    self.module_status = json.dumps(beams_status)
                    self.save()
                    answer = 0
                    return 0
        else:
            self.message = "ABS Configuration does not have beams"
            return 0

        #self.device.status = 1
        ##
        if answer==1:
            self.message = "ABS Beams List have been sent to ABS Modules"
            beams[0].set_as_activebeam()
        else:
            self.message = "Could not read ABS parameters"
        ##
        self.save()
        return 1




    def read_module(self, module):

        """
        Read out-bits (up-down) of 1 abs module NOT for Configuration
        """

        parameters = {}
        ip_address  = self.device.ip_address
        ip_address  = ip_address.split('.')
        module_seq  = (ip_address[0],ip_address[1],ip_address[2])
        dot         = '.'
        module_ip   = dot.join(module_seq)+'.'+str(module)
        module_port = self.device.port_address
        read_route = 'http://'+module_ip+':'+str(module_port)+'/read'

        print(read_route)

        answer = ''
        module_bits = ''

        try:
            r_write = requests.get(read_route, timeout=0.7)
            answer  = r_write.json()
            self.message = answer['message']
            module_bits    = answer['allbits']
        except:
            #message = "Could not read ABS parameters"
            answer  = r_write.json()
            return 0

        return module_bits


    def absmodule_status(self):
        """
        This function gets the status of each abs module. It sends GET method to Web Application
        in Python Bottle.
        This function updates "module_status" field from ABSconfiguration.
        """
        ip_address  = self.device.ip_address
        ip_address  = ip_address.split('.')
        module_seq  = (ip_address[0],ip_address[1],ip_address[2])
        dot         = '.'
        module_port = self.device.port_address

        modules_status = json.loads(self.module_status)

        for i in range(1,65):
            module_ip   = dot.join(module_seq)+'.'+str(i)
            print module_ip

            route = 'http://'+module_ip+':'+str(module_port)+'/hello'

            try:
                r = requests.get(route, timeout=0.7)
                modules_status[str(i)] = 1
            except:
                modules_status[str(i)] = 0
                pass


        self.module_status=json.dumps(modules_status)
        self.save()

        return


    def connected_modules(self):
        """
        This function returns the number of connected abs-modules without updating.
        """
        modules_status = json.loads(self.module_status)
        num = 0
        for status in modules_status:
            num = num +modules_status[status]

        return num


    def status_device(self):
        """
        This function returns the status of all abs-modules as one.
        If at least one module is connected, its answer is "1"
        """
        self.absmodule_status()
        connected_modules = self.connected_modules()
        if connected_modules>0:
            self.message = 'ABS modules Status have been updated.'
            return 1
        self.message = 'No ABS module is connected.'
        return 0



    def write_module(self, module):

        """
        Send configuration to one abs module
        """

        parameters = {}
        ip_address  = self.abs_conf.device.ip_address
        ip_address  = ip_address.split('.')
        module_seq  = (ip_address[0],ip_address[1],ip_address[2])
        dot         = '.'
        module_ip   = dot.join(module_seq)+'.'+str(module)
        module_port = self.abs_conf.device.port_address
        write_route = 'http://'+module_ip+':'+str(module_port)+'/write'

        #print write_route

        header = 'JROABSCeCnModCnMod01000108SNDFexperimento1.ab1'
        module = 'ABS_'+str(module)
        beams  = {1: '001000', 2: '010001', 3: '010010', 4: '000011', 5: '101100', 6: '101101',
                  7: '110110', 8: '111111', 9: '000000', 10: '001001', 11: '010010', 12: '011011'}

        parameters['header'] = header
        parameters['module'] = module
        parameters['beams']  = json.dumps(beams)

        answer = ''

        try:
            r_write = requests.post(write_route, parameters, timeout=0.5)
            answer  = r_write.json()
            self.message = answer['message']
        except:
            self.message = "Could not write ABS parameters"
            return 0


        #self.device.status = int(answer['status'])

        return 1


    def beam_selector(self, module, beam_pos):
        """
        This function selects the beam number for one absmodule.
        """

        if beam_pos > 0:
            beam_pos = beam_pos - 1
        else:
            beam_pos = 0

        #El indice del apunte debe ser menor que el numero total de apuntes
        #El servidor tcp en el embebido comienza a contar desde 0
        beams_list    = ABSBeam.objects.filter(abs_conf=self)
        if len(beams_list) < beam_pos:
            return 0

        flag = 1
        if beam_pos>9:
            flag = 2

        module_address = ('192.168.1.'+str(module), 5500)
        header   = 'JROABSCeCnModCnMod0100000'
        numbers  = len(str(beam_pos))
        function = 'CHGB'

        message_tx = header+str(numbers)+function+str(beam_pos)+'0'

        # Create the datagram socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #sock.connect(module_address)
        try:
            sock.connect(module_address)
            sock.send(message_tx)
            sock.close()
            print("Writing abs module:"+module_address[0]+"...")
        except:
            sock = None
            print("Problem writing abs module:"+module_address[0])
            return 0

        return 1


    def change_beam(self, beam_pos):
        """
        This function selects the beam number for all absmodules.
        """
        for i in range(1,65):
            try:
                self.beam_selector(i,beam_pos)
            except:
                print("Problem with module: 192.168.1."+str(i))
                self.message = "Problem with module: 192.168.1."+str(i)
                #return 0
        return 1


    def send_beam_num(self, beam_pos):
        """
        This function connects to a multicast group and sends the beam number
        to all abs modules.
        """

        if beam_pos > 0:
            beam_pos = beam_pos - 1
        else:
            beam_pos = 0

        #El indice del apunte debe ser menor que el numero total de apuntes
        #El servidor tcp en el embebido comienza a contar desde 0
        beams_list    = ABSBeam.objects.filter(abs_conf=self)
        if len(beams_list) < beam_pos:
            return 0

        flag = 1
        if beam_pos>9:
            flag = 2

        header   = 'JROABSCeCnModCnMod0100000'
        flag  = str(flag)
        function = 'CHGB'
        message_tx = header+flag+function+str(beam_pos)+'0'

        multicast_group = '224.3.29.71'
        server_address = ('',10000)

        # Create the socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Bind to the server address
        sock.bind(server_address)
        # Telling the OS add the socket to the multicast on all interfaces
        group = socket.inet_aton(multicast_group)
        mreq  = struct.pack('4sL', group, socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        #print 'sending acknowledgement to all: \n' + message_tx
        sock.sendto(message_tx, (multicast_group, 10000))
        sock.close()
        sock = None

        return 1

    def test1(self):
        t1 = time.time()
        t2 = 0
        while (t2-t1)<100:#300
            t2 = time.time()
            self.send_beam_num(2)
            time.sleep(0.04)
            self.send_beam_num(1)
            time.sleep(0.04)
        return

    def change_procs_test1(self, module):

    	for i in range (1,300):#300
    	    beam_pos = 1
    	    module_address = ('192.168.1.'+str(module), 5500)
    	    header   = 'JROABSCeCnModCnMod0100000'
    	    numbers  = len(str(beam_pos))
    	    function = 'CHGB'

    	    message_tx = header+str(numbers)+function+str(beam_pos)+'0'

    	    # Create the datagram socket
    	    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    	    sock.connect(module_address)

    	    sock.send(message_tx)
    	    #t = sock.recv(1024)
    	    sock.close()
    	    sock = None


    	    time.sleep(0.04)


    	    beam_pos = 0
    	    numbers  = len(str(beam_pos))

    	    message_tx = header+str(numbers)+function+str(beam_pos)+'0'

    	    # Create the datagram socket
    	    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    	    sock.connect(module_address)
    	    sock.send(message_tx)
    	    sock.close()
    	    sock = None

    	    time.sleep(0.04)


    def multi_procs_test1(self):

        """
        This function sends the beam number to all abs modules using multiprocessing.
        """

        #if __name__ == "__main__":
        size = 10000000   # Number of random numbers to add
        procs =  65 # (Number-1) of processes to create (absmodule)

        # Create a list of jobs and then iterate through
        # the number of processes appending each process to
        # the job list
        jobs = []
        for i in range(1, procs):

            process = multiprocessing.Process(target=self.change_procs_test1,args=(i,))
            jobs.append(process)
            #print jobs

            # Start the processes (i.e. calculate the random number lists)
        for j in jobs:
                #time.sleep(0.4)
                #print j
                j.start()

            # Ensure all of the processes have finished
        for j in jobs:
                j.join()

        print("List processing complete.")
        return 1



    def multi_procs_test2(self):
        """
        This function use multiprocessing python library. Importing Pool we can select
        the number of cores we want to use
        After 'nproc' linux command, we know how many cores computer has.
        NOT WORKING
        """
        import multiprocessing
        pool = multiprocessing.Pool(3) # cores

        tasks = []
        procs = 65
        for i in range(62, procs):
            tasks.append( (i,))
        #print tasks
        #pool.apply_async(self.change_procs_test1, 62)
        results = [pool.apply( self.change_procs_test1, t ) for t in tasks]
        #for result in results:
            #result.get()
            #(plotNum, plotFilename) = result.get()
            #print("Result: plot %d written to %s" % (plotNum, plotFilename) )

        return 1


    def multi_procs_test3(self):
        """
        This function use multiprocessing python library. Importing Pool we can select
        the number of cores we want to use
        After 'nproc' linux command, we know how many cores computer has.
        """
        from multiprocessing import Pool
        import time

        def f(x):
            return x*x

        tasks = []
        procs = 65
        pool = Pool(processes=4)

        #for i in range(62, procs):
        #result = pool.map(f, range(62,65))
        it = pool.imap(self.change_procs_test1, range(62,65))
        #result.get(timeout=5)

        return 1


    def f(x):
        print x
        return

    def multi_procs_test4(self):
        import multiprocessing as mp


        num_workers = mp.cpu_count()

        pool = mp.Pool(num_workers)
        procs = 65
        for i in range(62, procs):
        #for task in tasks:
            pool.apply_async(self.f, args = (i,))

        pool.close()
        pool.join()

        return 1


    def get_absolute_url_import(self):
        return reverse('url_import_abs_conf', args=[str(self.id)])




class ABSBeam(models.Model):

    name         = models.CharField(max_length=60, default='Beam')
    antenna      = models.CharField(verbose_name='Antenna', max_length=1000, default=antenna_default)
    abs_conf     = models.ForeignKey(ABSConfiguration, null=True, verbose_name='ABS Configuration')
    tx           = models.CharField(verbose_name='Tx', max_length=1000, default=tx_default)
    rx           = models.CharField(verbose_name='Rx', max_length=1000, default=rx_default)
    s_time       = models.TimeField(verbose_name='Star Time', default='00:00:00')
    e_time       = models.TimeField(verbose_name='End Time', default='23:59:59')
    modules_conf = models.CharField(verbose_name='Modules', max_length=2000, default=json.dumps(conf_default))
    ues          = models.CharField(verbose_name='Ues', max_length=100, default=ues_default)
    only_rx      = models.CharField(verbose_name='Only RX', max_length=40, default=onlyrx_default)

    class Meta:
        db_table = 'abs_beams'

    def __unicode__(self):
        return u'%s' % (self.name)

    def parms_to_dict(self):

        #Update data
        self.modules_6bits()

        parameters = {}

        parameters['name']          = self.name
        parameters['antenna']       = ast.literal_eval(self.antenna)
        parameters['abs_conf']      = self.abs_conf.name
        parameters['tx']            = ast.literal_eval(self.tx)
        parameters['rx']            = ast.literal_eval(self.rx)
        parameters['s_time']        = self.s_time.strftime("%H:%M:%S")
        parameters['e_time']        = self.e_time.strftime("%H:%M:%S")
        parameters['configuration'] = ast.literal_eval(self.modules_conf)
        parameters['ues']           = ast.literal_eval(self.ues)
        parameters['only_rx']       = json.loads(self.only_rx)

        return parameters

    def dict_to_parms(self, parameters):

        self.name     = parameters['name']
        self.antenna  = json.dumps(parameters['antenna'])
        #self.abs_conf = parameters['abs_conf']
        self.tx       = json.dumps(parameters['tx'])
        self.rx       = json.dumps(parameters['rx'])
        #self.s_time = parameters['s_time']
        #self.e_time = parameters['e_time']
        self.ues      = json.dumps(parameters['ues'])
        self.only_rx     = json.dumps(parameters['only_rx'])

        self.modules_6bits()
        self.save()


    def clone(self, **kwargs):

        self.pk = None
        self.id = None
        for attr, value in kwargs.items():
            setattr(self, attr, value)

        self.save()

        return self



    def module_6bits(self, module):
        """
        This function reads antenna pattern and choose 6bits (upbits-downbits) for one abs module
        """
        if module > 64:
            beam_bits = ""
            return beam_bits

        data      = ast.literal_eval(self.antenna)
        up_data   = data['antenna_up']
        down_data = data['antenna_down']

        pos        = ip2position(module)
        up_value   = up_data[pos[0]][pos[1]]
        down_value = down_data[pos[0]][pos[1]]

        up_bits   = up_conv_bits(up_value)
        down_bits = down_conv_bits(down_value)
        beam_bits = up_bits+down_bits

        return beam_bits

    def modules_6bits(self):
        """
        This function returns 6bits from every abs module (1-64) in a dict
        """
        modules_configuration = ast.literal_eval(self.modules_conf)

        for i in range(1,65):
            modules_configuration[str(i)] =  self.module_6bits(i)

        self.modules_conf = json.dumps(modules_configuration)
        self.save()

        return self.modules_conf


    def set_as_activebeam(self):
        """
        This function set this beam as the active beam of its ABS Configuration.
        """
        self.abs_conf.active_beam = json.dumps({'active_beam': self.id})
        self.abs_conf.save()

        return


    @property
    def get_upvalues(self):
        """
        This function reads antenna pattern and show the up-value of one abs module
        """

        data      = ast.literal_eval(self.antenna)
        up_data   = data['antenna_up']

        up_values = []
        for data in up_data:
            for i in range(0,8):
                up_values.append(data[i])

        return up_values

    @property
    def antenna_upvalues(self):
        """
        This function reads antenna pattern and show the up - values of one abs beam
        in a particular order
        """
        data      = ast.literal_eval(self.antenna)
        up_data   = data['antenna_up']

        return up_data

    @property
    def antenna_downvalues(self):
        """
        This function reads antenna pattern and show the down - values of one abs beam
        in a particular order
        """
        data      = ast.literal_eval(self.antenna)
        down_data   = data['antenna_down']

        return down_data

    @property
    def get_downvalues(self):
        """
        This function reads antenna pattern and show the down-value of one abs module
        """

        data      = ast.literal_eval(self.antenna)
        down_data = data['antenna_down']

        down_values = []
        for data in down_data:
            for i in range(0,8):
                down_values.append(data[i])

        return down_values

    @property
    def get_up_ues(self):
        """
        This function shows the up-ues-value of one beam
        """
        data      = ast.literal_eval(self.ues)
        up_ues = data['up']

        return up_ues

    @property
    def get_down_ues(self):
        """
        This function shows the down-ues-value of one beam
        """
        data      = ast.literal_eval(self.ues)
        down_ues = data['down']

        return down_ues

    @property
    def get_up_onlyrx(self):
        """
        This function shows the up-onlyrx-value of one beam
        """
        data      = json.loads(self.only_rx)
        up_onlyrx = data['up']

        return up_onlyrx

    @property
    def get_down_onlyrx(self):
        """
        This function shows the down-onlyrx-value of one beam
        """
        data      = json.loads(self.only_rx)
        down_onlyrx = data['down']

        return down_onlyrx

    @property
    def get_tx(self):
        """
        This function shows the tx-values of one beam
        """
        data = json.loads(self.tx)

        return data

    @property
    def get_uptx(self):
        """
        This function shows the up-tx-values of one beam
        """
        data = json.loads(self.tx)
        up_data = data['up']

        up_values = []
        for data in up_data:
            for i in range(0,8):
                up_values.append(data[i])

        return up_values

    @property
    def get_downtx(self):
        """
        This function shows the down-tx-values of one beam
        """
        data = json.loads(self.tx)
        down_data = data['down']

        down_values = []
        for data in down_data:
            for i in range(0,8):
                down_values.append(data[i])

        return down_values



    @property
    def get_rx(self):
        """
        This function shows the rx-values of one beam
        """
        data = json.loads(self.rx)

        return data

    @property
    def get_uprx(self):
        """
        This function shows the up-rx-values of one beam
        """
        data = json.loads(self.rx)
        up_data = data['up']

        up_values = []
        for data in up_data:
            for i in range(0,8):
                up_values.append(data[i])

        return up_values

    @property
    def get_downrx(self):
        """
        This function shows the down-rx-values of one beam
        """
        data = json.loads(self.rx)
        down_data = data['down']

        down_values = []
        for data in down_data:
            for i in range(0,8):
                down_values.append(data[i])

        return down_values
