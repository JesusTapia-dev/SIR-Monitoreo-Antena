'''
'''

import json
import os
import math

from apps.main.utils import Params

DECODE_TYPE = {'DECODING_TIME_DOMAIN': 1, 'DECODING_FREQ_DOMAIN': 2, 'DECODING_INV_FREQ_DOMAIN': 3}

def parse_range(s):

    vars = ('TXA,', 'A,', 'TXB,', 'B,', 'TXA', 'TXB', 'A', 'B')

    for var in vars:
        if var in s:
            s = s.replace(var, '')
            if 'A' in var:
                ref = 'TXA'
            else:
                ref = 'TXB'
            return ref, s

    return '0', s


class RacpFile(object):
    '''
    Class to handle Radar controller configuration files
    '''

    def __init__(self, f=None):
        #print dir(f)
        self.data = {}
        self.lines = []
        self.line = ''
        if isinstance(f, str):
            self.f = open(f)
            self.name = f.split('/')[-1]
        elif hasattr(f, 'read'):
            self.f = f
            self.name = f.name.split('/')[-1]
        else:
            self.f = f
            self.name = None

        if self.f:
            if 'racp' in self.name:
                self.parse_racp()
            elif 'dat' in self.name:
                self.parse_dat()
            elif 'json' in self.name:
                self.data = json.load(self.f)

        self.f.close()

    def get_line_parameters(self, data, line):

        line_params = {}
        for label in data:
            if 'L%d' % line in label or '(Line %d)' % line in label or 'Line%d' % line in label:
                line_params[label] = data[label]
        return line_params

    def parse_racp(self):

        data = {}
        raw_data =  [s.strip() for s in self.f.readlines()]

        for line in raw_data:
            if line and '=' in line:
                label, value = line.strip().split('=')
                data[label] = value

        self.data['id'] = '1'
        self.data['device_type'] = 'jars'
        self.data['experiment_type'] = data['EXPERIMENT TYPE']
        self.data['header_version'] = data['HEADER VERSION']
        self.data['name'] = data['EXPERIMENT NAME']
        self.data['ipp'] = float(data['IPP'])
        self.data['ntx'] = int(data['NTX'])
        
        #----Jars parameters----
        self.data['cards_number']    = data['Number of Cards']
        self.data['channels_number'] = data['Number of Channels']

        channels = ''
        for i in range(0,20):
            try:
                channels += data['Channel('+str(i)+')']+','
            except:
                break
        if channels:
            channels = channels[:-1]
        self.data['channels']     = channels
        
        data_type = 0
        if data['DATATYPE'] == 'FLOAT':
            data_type = 1
        self.data['data_type'] = data_type
        
        self.data['profiles_block']  = data['PROFILES PER BLOCK']
        self.data['acq_profiles']    = data['ACQUIRED PROFILES']
        self.data['ftp_interval']    = data['FTP INTERVAL']
        self.data['cohe_integr_str'] = data['COHERENT INTEGRATION STRIDE']

        self.data['cohe_integr'] = 1
        if 'COHERENT INTEGRATIONS' in data:
            if int(data['COHERENT INTEGRATIONS']) != 0:
                self.data['cohe_integr'] = int(data['COHERENT INTEGRATIONS'])
        
        self.data['exp_type']                = 0
        if data['EXPERIMENT TYPE'] != 'EXP_RAW_DATA':
            self.data['exp_type']        = 1
            self.data['fftpoints']       = data['FFTPOINTS']
            self.data['incohe_integr']   = data['INCOHERENT INTEGRATIONS']
            self.data['spectral_number'] = data['TOTAL SPECTRAL COMBINATIONS']

            spectral = ''
            for i in range(0,100):
                try:
                    spectral += '['+data['SPEC_COMB('+str(i)+')']+'],'
                except:
                    break
            self.data['spectral'] = spectral
            self.data['save_ch_dc'] = False
            if 'SAVE CHANNELS DC' in data:
                self.data['save_ch_dc'] = True
        else:
            self.data['raw_data_blocks'] = data['RAW DATA BLOCKS']
        
        self.data['decode_data'] = 0
        self.data['post_coh_int'] = False
        if 'DECODE DATA' in data:
            self.data['decode_data'] = DECODE_TYPE[data['DECODING TYPE']]
            if 'POST COHERENT INTEGRATIONS' in data:
                self.data['post_coh_int'] = True
        
        self.data['create_directory'] = False
        if data['CREATE DIRECTORY PER DAY'] == 'YES':
            self.data['create_directory'] = True
        
        self.data['include_expname'] = False
        if data['INCLUDE EXPNAME IN DIRECTORY'] == 'YES':
            self.data['include_expname'] = True
        
        self.data['save_data'] = False
        if data['SAVE DATA'] == 'YES':
            self.data['save_data'] = True
        #----Jars parameters----
        

        if 'CLOCK DIVIDER' in data:
            self.data['clock_divider'] = int(data['CLOCK DIVIDER'])
        else:
            self.data['clock_divider'] = 1
        self.data['clock_in'] = float(data['RELOJ'])*self.data['clock_divider']
        self.data['clock'] = float(data['RELOJ'])
        self.data['time_before'] = int(data['TR_BEFORE'])
        self.data['time_after'] = int(data['TR_AFTER'])

        if 'SYNCHRO DELAY' in data:
            self.data['sync'] = int(data['SYNCHRO DELAY'])
        else:
            self.data['sync'] = 0

        self.data['lines'] = []

        if 'SAMPLING REFERENCE' in data:
            if data['SAMPLING REFERENCE']=='MIDDLE OF FIRST BAUD':
                self.data['sampling_reference'] = 'first_baud'
            elif data['SAMPLING REFERENCE']=='MIDDLE OF FIRST SUB-BAUD':
                self.data['sampling_reference'] = 'sub_baud'
            else:
                self.data['sampling_reference'] = 'none'

        self.data['lines'].append('10')

        #Add TX's lines
        if 'TXA' in data:
            line = {'line_type':'tx', 'id':'11', 'name':'TXA',
              'params':{'pulse_width':data['TXA'], 'delays':'0', 'range':'0'}}
            if 'Pulse selection_TXA' in data:
                line['params']['range'] = data['Pulse selection_TXA']
            self.data['lines'].append('11')
            self.lines.append(line)

        if 'TXB' in data:
            line = {'line_type':'tx', 'id':'12', 'name':'TXB',
              'params':{'pulse_width':data['TXB'], 'delays':'0', 'range':'0'}}
            if 'Pulse selection_TXB' in data:
                line['params']['range'] = data['Pulse selection_TXB']

            if 'Number of Taus' in data:
                delays = [data['TAU({0})'.format(i)] for i in range(int(data['Number of Taus']))]
                line['params']['delays'] = ','.join(delays)

            self.data['lines'].append('12')
            self.lines.append(line)

        #Add TR line
        line = {'line_type':'tr', 'id':'10', 'name':'TR',
              'params':{'TX_ref':'0', 'range':'0'}}
        if 'Pulse selection_TR' in data:
            ref, rng = parse_range(data['Pulse selection_TR'])
            line['params']['range'] = rng if rng else '0'
            if ref=='TXA':
                line['params']['TX_ref'] = '11'
            elif ref=='TXB':
                line['params']['TX_ref'] = '12'

        self.lines.append(line)

        #Add Other lines (4-6)
        for n in range(4, 7):
            id = '{:2d}'.format(10*n)
            params = self.get_line_parameters(data, n)
            labels = params.keys()

            if 'L%d_FLIP' % n in labels:
                line = {'line_type':'flip', 'id':id,
                  'params':{'number_of_flips':data['L%d_FLIP' % n]}}
            elif 'Code Type' in data and n==4:
                line = {'line_type':'codes', 'id':id, 'params':{'code':data['Code Type']}}
                if data['L%d_REFERENCE' % n]=='TXA':
                    line['params']['TX_ref'] = '11'
                else:
                    line['params']['TX_ref'] = '12'
                if 'Number of Codes' in data:
                    line['params']['codes'] = [data['COD({})'.format(x)] for x in range(int(data['Number of Codes']))]
            elif 'Code Type (Line %d)' % n in labels:
                line = {'line_type':'codes', 'id':id, 'params':{'code':data['Code Type (Line %d)' % n]}}
                if data['L%d_REFERENCE' % n]=='TXA':
                    line['params']['TX_ref'] = '11'
                else:
                    line['params']['TX_ref'] = '12'
                if 'Number of Codes (Line %d)' % n in data:
                    line['params']['codes'] = [data['L{}_COD({})'.format(n, x)] for x in range(int(data['Number of Codes (Line %d)' % n]))]
            elif 'Sampling Windows (Line %d)' % n in data:
                line = {'line_type':'windows', 'id':id, 'params':{}}
                if data['L%d_REFERENCE' % n]=='TXA':
                    line['params']['TX_ref'] = '11'
                else:
                    line['params']['TX_ref'] = '12'
                windows = []
                for w in range(int(data['Sampling Windows (Line %d)' % n])):
                    windows.append({'first_height':float(data['L%d_H0(%d)' % (n, w)]),
                         'resolution':float(data['L%d_DH(%d)' % (n, w)]),
                         'number_of_samples':int(float(data['L%d_NSA(%d)' % (n, w)])),
                         'last_height':float(data['L%d_DH(%d)' % (n, w)])*(int(float(data['L%d_NSA(%d)' % (n, w)]))-1)+float(data['L%d_H0(%d)' % (n, w)])
                         }
                        )
                line['params']['params'] = windows
            elif 'Line%d' % n in labels and data['Line%d' % n]=='Synchro':
                line = {'line_type':'sync', 'id':id, 'params':{'invert':0}}
            elif 'L%d Number Of Portions' % n in labels:
                line = {'line_type':'prog_pulses', 'id':id, 'params':{}}
                if 'L%s Portions IPP Periodic' % n in data:
                    line['params']['periodic'] = '1' if data['L%s Portions IPP Periodic' % n]=='YES' else '0'
                portions = []
                x = raw_data.index('L%d Number Of Portions=%s' % (n, data['L%d Number Of Portions' % n]))
                for w in range(int(data['L%d Number Of Portions' % n])):
                    begin = float(raw_data[x+1+2*w].split('=')[-1])
                    end = float(raw_data[x+2+2*w].split('=')[-1])
                    portions.append({'begin':int(begin),
                         'end':int(end)}
                        )
                line['params']['params'] = portions
            elif 'FLIP1' in data and n==5:
                line = {'line_type':'flip', 'id':id, 'params':{'number_of_flips':data['FLIP1']}}
            elif 'FLIP2' in data and n==6:
                line = {'line_type':'flip', 'id':id, 'params':{'number_of_flips':data['FLIP2']}}
            else:
                line = {'line_type':'none', 'id':id, 'params':{}}

            self.data['lines'].append(id)
            self.lines.append(line)

        #Add line 7 (windows)
        if 'Sampling Windows' in data:
            line = {'line_type':'windows', 'id':'17', 'params':{}}
            if data['L7_REFERENCE']=='TXA':
                line['params']['TX_ref'] = '11'
            else:
                line['params']['TX_ref'] = '12'
            windows = []
            x = raw_data.index('Sampling Windows=%s' % data['Sampling Windows'])
            for w in range(int(data['Sampling Windows'])):
                h0 = raw_data[x+1+3*w].split('=')[-1]
                nsa = raw_data[x+2+3*w].split('=')[-1]
                dh = raw_data[x+3+3*w].split('=')[-1]
                windows.append({'first_height':float(h0),
                     'number_of_samples':int(nsa),
                     'resolution':float(dh),
                     'last_height':float(h0)+float(dh)*(int(nsa)-1)}
                    )
            line['params']['params'] = windows
            self.data['lines'].append('17')
            self.lines.append(line)

        #Add line 8 (synchro inverted)
        self.data['lines'].append('18')
        self.lines.append({'line_type':'sync', 'id':'18', 'params':{'invert':1}})

        return

    def parse_dat(self):
        pass

    def to_dict(self):

        out = Params()
        out.add(self.data, 'configurations')
        for line_data in self.lines:
            out.add(line_data, 'lines')

        return out.data




def parse_line(n, data, lines):

    line_text = ''
    line_type = data['lines']['byId'][lines[n]]['line_type']
    num = n+1
    if line_type == 'windows':
        if num == 7:
            reference = data['lines']['byId'][lines[n]]['params']['TX_ref']
            windows = data['lines']['byId'][lines[n]]['params']['params']
            if windows:
                dh = str(float(windows[0]['resolution']))
            else:
                dh = ''

            line_text = 'Sampling Windows={}\n'.format(len(windows))

            cnt = 0
            for window in windows:
                line_text += ('H0({cnt})={first_height}\n'
                    'NSA({cnt})={number_of_samples}\n'
                    'DH({cnt})={dh}\n'.format(
                        cnt=cnt,
                        first_height=window['first_height'],
                        number_of_samples=int(window['number_of_samples']),
                        dh=dh
                        )
                    )
                cnt += 1

        else:
            reference = data['lines']['byId'][lines[n]]['params']['TX_ref']
            windows = data['lines']['byId'][lines[n]]['params']['params']
            if windows:
                dh = str(float(windows[0]['resolution']))
            else:
                dh = ''

            line_text = 'Sampling Windows (Line {})={}\n'.format(num, len(windows))

            cnt = 0
            for window in windows:
                line_text += ('L{num}_H0({cnt})={first_height}\n'
                    'L{num}_NSA({cnt})={number_of_samples}\n'
                    'L{num}_DH({cnt})={dh}\n'.format(
                        num=num,
                        cnt=cnt,
                        first_height=window['first_height'],
                        number_of_samples=int(window['number_of_samples']),
                        dh=dh
                        )
                    )
                cnt += 1

        line_text += 'L{}_REFERENCE={}\n'.format(
            num,
            data['lines']['byId'][reference]['name']
        )

    elif line_type == 'sync':
        line_text = 'Line{}=Synchro\n'.format(num)

    elif line_type == 'flip':
        line_text = 'L{}_FLIP={}\n'.format(
            num,
            data['lines']['byId'][lines[n]]['params']['number_of_flips']
        )

    elif line_type == 'prog_pulses':
        periodic = data['lines']['byId'][lines[n]]['params']['periodic']
        if periodic == '0':
            periodic = 'NO'
        else:
            periodic = 'YES'

        portions = data['lines']['byId'][lines[n]]['params']['params']
        line_text = 'L{} Number Of Portions={}\n'.format(num, len(portions))

        for i, portion in enumerate(portions):
            line_text += 'PORTION_BEGIN({cnt})={begin}\nPORTION_END({cnt})={end}\n'.format(
                cnt=i,
                begin=int(portion['begin']),
                end=int(portion['end']),
            )

        line_text += 'L{} Portions IPP Periodic={}\n'.format(num, periodic)

    elif line_type == 'none':
        line_text = ''

    else:
        reference = data['lines']['byId'][lines[n]]['params']['TX_ref']
        code_type = data['lines']['byId'][lines[n]]['params']['code']
        codes = data['lines']['byId'][lines[n]]['params']['codes']

        if num == 4:
            line_text = 'Code Type={}\n'.format(code_type)
            line_text += 'Number of Codes={}\nCode Width={}\n'.format(
                len(codes),
                len(codes[0])
            )
            cnt = 0
            for code in codes:
                line_text += 'COD({})={}\n'.format(cnt, code)
                cnt += 1
        else:
            line_text = 'Code Type (Line {})={}\n'.format(num, code_type)
            line_text += 'Number of Codes (Line {})={}\nCode Width (Line {})={}\n'.format(
                num,
                len(codes),
                num,
                len(codes[0])
            )
            cnt = 0
            for code in codes:
                line_text += 'L{}_COD({})={}\n'.format(num,cnt, code)
                cnt += 1

        line_text += 'L{}_REFERENCE={}\n'.format(
            num,
            data['lines']['byId'][reference]['name']
        )

    return line_text

def create_jarsfiles(json_data):
    """
	Function to create *.racp and *.jars files with json_data
	"""
    #global EXPNAME

    data = json.loads(json_data)
    exp_id = data['experiments']['allIds'][0]
    experiment = data['experiments']['byId'][exp_id]
    name = experiment['name']
    #EXPNAME = name
    folder_name = name#os.path.join(PATH, name)
    #print 'Experiment: ' + name + ' received...'
    #if not os.path.exists(folder_name):
    #    os.makedirs(folder_name)
    #print 'Folder OK'
    #if not os.path.exists(folder_name+'/DATA'):
    #    os.mkdir(folder_name+'/DATA')

    #try:
    #    racp_file = open(folder_name+'/'+name+'_jars.racp', 'w')
    #except:
    #    return 0, 'Error creating .racp file'

    #try:
    #    json_file = open(folder_name+'/'+name+'_jars.json', 'w')
    #except:
    #    return 0, 'Error creating .json file'

    #json_file.write(json_data)
    #json_file.close()

    conf_ids = data['configurations']['allIds']

    rc_id = [pk for pk in conf_ids \
        if data['configurations']['byId'][pk]['device_type'] == 'rc'][0]

    jars_id = [pk for pk in conf_ids \
        if data['configurations']['byId'][pk]['device_type'] == 'jars'][0]

    rc = data['configurations']['byId'][rc_id]
    jars = data['configurations']['byId'][jars_id]

    if rc['mix'] == 'True':
        mix_text = '*******Mixed Experiment*******************\n'
        mix_text += '*******System parameters******************\n'
    else:
        mix_text = ''

    exp_type = jars['exp_type']
    if exp_type == 0:
        exp_type = 'EXP_RAW_DATA'
    else:
        exp_type = 'EXP_PROCESS_SPECTRA'

    racp_text = 'EXPERIMENT TYPE={}\nEXPERIMENT NAME={}\nHEADER VERSION=1103\n'.format(
        exp_type,
        name
    )

    racp_text += '*****Radar Controller Parameters**********\n{}'.format(mix_text)
    racp_text += 'IPP={}\n'.format(float(rc['ipp']))
    racp_text += 'NTX={}\n'.format(rc['ntx'])
    racp_text += 'TXA={}\n'.format(
        data['lines']['byId'][rc['lines'][1]]['params']['pulse_width']
    )

    racp_text += 'TXB={}\n'.format(
        data['lines']['byId'][rc['lines'][2]]['params']['pulse_width']
    )

    idTR = data['lines']['byId'][rc['lines'][0]]['params']['TX_ref']
    rangeTR = data['lines']['byId'][rc['lines'][0]]['params']['range']

    if rangeTR != '0':
        racp_text += 'Pulse selection_TR={}\n'.format(rangeTR)
    elif idTR != '0':
        racp_text += 'Pulse selection_TR={}\n'.format(
            data['lines']['byId'][idTR]['name'][-1]
        )
    print 'TR OK'

    rangeTXA = data['lines']['byId'][rc['lines'][1]]['params']['range']
    if rangeTXA != '0':
        racp_text += 'Pulse selection_TXA={}\n'.format(rangeTXA)
    rangeTXB = data['lines']['byId'][rc['lines'][2]]['params']['range']
    if rangeTXB != '0': #if rangeTXB == '0':
        racp_text += 'Pulse selection_TXB={}\n'.format(rangeTXB)
    print 'Pulse selection OK'

    for n in range(3, 6):
        racp_text += parse_line(n, data, rc['lines'])

    taus = data['lines']['byId'][rc['lines'][2]]['params']['delays'].split(',')

    if taus != '0':
        racp_text += 'Number of Taus={}\n'.format(len(taus))
        for n, tau in enumerate(taus):
            racp_text += 'TAU({})={}\n'.format(n, tau)
    print 'Taus OK'

    racp_text += parse_line(6, data, rc['lines'])
    racp_text += 'SAMPLING REFERENCE=MIDDLE OF FIRST SUB-BAUD\n'
    racp_text += 'RELOJ={}\n'.format(int(rc['clock']))
    racp_text += 'CLOCK DIVIDER={}\n'.format(int(rc['clock_divider']))
    racp_text += 'TR_BEFORE={}\n'.format(rc['time_before'])
    racp_text += 'TR_AFTER={}\n'.format(rc['time_after'])
    racp_text += 'WINDOW IN LINE 5&6=NO\n'
    racp_text += '******System Parameters*******************\n'
    racp_text += 'Number of Cards={}\n'.format(jars['cards_number'])

    for i in range(jars['cards_number']):
        racp_text += 'Card({})={}\n'.format(i, i)

    channels = jars['channels'].split(',')

    if channels:
        racp_text += 'Number of Channels={}\n'.format(len(channels))
        for i, channel in enumerate(channels):
            racp_text += 'Channel({})={}\n'.format(i, channel)
    print 'Channels OK'

    if exp_type == 'EXP_RAW_DATA':
        racp_text += 'RAW DATA DIRECTORY={}\n'.format(os.path.join(folder_name, 'DATA'))
    else:
        racp_text += 'PROCESS DATA DIRECTORY={}\n'.format(os.path.join(folder_name, 'DATA'))

    if jars['create_directory']:
        racp_text += 'CREATE DIRECTORY PER DAY=YES'+'\n'
    else:
        racp_text += 'CREATE DIRECTORY PER DAY=NO'+'\n'

    if jars['include_expname']:
        racp_text += 'INCLUDE EXPNAME IN DIRECTORY=YES'+'\n'
    else:
        racp_text += 'INCLUDE EXPNAME IN DIRECTORY=NO'+'\n'

    racp_text += '******System Parameters*******************\n'
    racp_text += 'ADC Resolution=8\n'
    racp_text += 'PCI DIO BusWidth=32\n'

    if exp_type == 'EXP_RAW_DATA':
        racp_text += 'RAW DATA BLOCKS={}\n'.format(jars['raw_data_blocks'])
        spectra_text = ''
    else:
        racp_text += 'PROCESS DATA BLOCKS=100\n'
        spectra_text = '------------------------------------------\n'

        if jars['fftpoints'] > 1:
            spectra_text += 'FFTPOINTS={}\n'.format(jars['fftpoints'])

        if jars['incohe_integr']:
            spectra_text += 'INCOHERENT INTEGRATIONS={}\n'.format(jars['incohe_integr'])

        if jars['save_ch_dc']:
            spectra_text += 'SAVE CHANNELS DC=YES\n'

        spectral = json.loads(jars['spectral'][:-1])
        if spectral:
            spectra_text += '------------------------------------------\n'
            spectra_text += 'TOTAL SPECTRAL COMBINATIONS={}\n'.format(len(spectral))
            for i, spc in enumerate(spectral):
                spectra_text += 'SPEC_COMB({})={},{}\n'.format(i, *spc)

    racp_text += '******Process Parameters******************\n'

    data_type = jars['data_type']

    if data_type == 0:
        racp_text += 'DATATYPE=SHORT\n'
    elif data_type == 1:
        racp_text += 'DATATYPE=FLOAT\n'
    print 'Datatype OK'

    racp_text += 'DATA ARRANGE=CONTIGUOUS_CH\n'

    if jars['cohe_integr'] > 1:
        racp_text += 'COHERENT INTEGRATIONS={}\n'.format(jars['cohe_integr'])

    decode_text = ''
    decode_data = jars['decode_data']
    if decode_data !=0:
        decode_text = 'DECODE DATA=YES\n'
        decode_text += 'DECODING TYPE={}\n'.format(DECODE_TYPE[decode_data])
        if jars['post_coh_int'] == True:
            decode_text += 'POST COHERENT INTEGRATIONS=YES\n'
        decode_text += '------------------------------------------\n'
    print 'Decode OK'

    racp_text += 'COHERENT INTEGRATION STRIDE={}\n'.format(jars['cohe_integr_str'])
    racp_text += '------------------------------------------\n'
    racp_text += 'ACQUIRED PROFILES={}\n'.format(jars['acq_profiles'])
    racp_text += 'PROFILES PER BLOCK={}\n'.format(jars['profiles_block'])
    racp_text += spectra_text
    racp_text += '------------------------------------------\n'
    racp_text += decode_text
    racp_text += 'BEGIN ON START=NO\n'
    racp_text += 'BEGIN_TIME={}\n'.format(experiment['start_time'][:-3])
    racp_text += 'END_TIME={}\n'.format(experiment['end_time'][:-3])
    racp_text += 'GENERATE ACQUISITION LINK=YES\n'
    racp_text += 'VIEW RAW DATA=YES\n'
    racp_text += 'REFRESH RATE=1\n'
    racp_text += '------------------------------------------\n'
    racp_text += 'SEND STATUS TO FTP=YES\n'
    racp_text += 'FTP SERVER=jro.igp.gob.pe\n'
    racp_text += 'FTP USER=wmaster\n'
    racp_text += 'FTP PASSWD=PKQLX20\n'
    racp_text += 'FTP DIR=/users/database/on-line/\n'
    racp_text += 'FTP FILE=status.txt\n'
    racp_text += 'FTP INTERVAL={}\n'.format(jars['ftp_interval'])
    racp_text += 'SAVE STATUS AND BLOCK=YES\n'
    racp_text += 'GENERATE RTI=YES\n'
    racp_text += 'RTI Inc.Int.=1\n'
    racp_text += 'SEND RTI AND BLOCK=YES\n'
    racp_text += '------------------------------------------\n'
    racp_text += 'COMPORT CONFIG=Com1 CBR_9600 TWOSTOPBITS NOPARITY\n'
    racp_text += 'JAM CONFIGURE FILE=dmasg_pprofiles_pch_64_pdigi_6clk.jam\n'
    racp_text += 'ACQUISITION SYSTEM=JARS\n'
    racp_text += '************JARS CONFIGURATION PARAMETERS************\n'

    #-------------------------JARS FILTER---------------------------------------
    filter_parms = jars['filter_parms']
    if filter_parms.__class__.__name__ == 'unicode':
        filter_parms = eval(filter_parms)
    elif filter_parms.__class__.__name__ == 'str':
        filter_parms = eval(filter_parms)
    if filter_parms.__class__.__name__ == 'str':
        filter_parms = eval(filter_parms)
    print 'Filter loaded OK'
    try:
        fclock = float(filter_parms['clock'])
        fch = float(filter_parms['fch'])
        m_dds = float(filter_parms['mult'])
        M_CIC2 = float(filter_parms['filter_2'])
        M_CIC5 = float(filter_parms['filter_5'])
        M_RCF = float(filter_parms['filter_fir'])
        print 'Filter parameters float OK'
    except:
        fclock = eval(filter_parms['clock'])
        fch = eval(filter_parms['fch'])
        m_dds = eval(filter_parms['mult'])
        M_CIC2 = eval(filter_parms['filter_2'])
        M_CIC5 = eval(filter_parms['filter_5'])
        M_RCF = eval(filter_parms['filter_fir'])
        print 'Filter parameters eval OK'

    filter_text = 'Loading\n'
    filter_text += 'Impulse file found -> C:\jars\F1MHZ_8_MATCH.imp\n'
    filter_text += 'Autoscale off\n'
    filter_text += 'Initialize Printer Port\n'
    filter_text += 'Chip Hardware Reset\n'
    filter_text += '300h -> 1\n'
    filter_text += '301h -> 6\n'
    filter_text += '302h -> 11111111111111111111111111111111\n'

    if abs(fch) < (fclock/2):
        nco = (2**32)*((fch/fclock))#%1)
        nco_i = long(nco)
    else:
        nco = (2**32)*(fclock-fch)/(fclock)
        nco_i = long(nco)

    filter_text += '303h -> {}\n'.format(nco_i)
    filter_text += '304h -> 0\n'
    
    input_level = 1
    S_CIC2  = math.ceil(math.log((M_CIC2**2)*input_level)/math.log(2))
    if S_CIC2 < 0:
        S_CIC2 = 0
    if S_CIC2 > 7:
        S_CIC2 = 7

    filter_text += '305h -> {}\n'.format(int(S_CIC2))
    filter_text += '306h -> {}\n'.format(int(M_CIC2-1))

    OL_CIC2 = input_level/(2.0**S_CIC2)

    S_CIC5 = math.ceil(math.log((M_CIC5**5)*OL_CIC2)/math.log(2))-5
    if S_CIC5 < 0:
        S_CIC5 = 0
    if S_CIC5 > 7:
        S_CIC5 = 7

    OL_CIC5 = ((M_CIC5**5)/(2**(S_CIC5+5)))*OL_CIC2

    filter_text += '307h -> {}\n'.format(int(S_CIC5))
    filter_text += '308h -> {}\n'.format(int(M_CIC5-1))

    Gain = 1
    S_RCF = int(4.0-math.log(Gain)/math.log(2))
    if S_RCF < 0:
        S_RCF = 0
    if S_RCF > 7:
        S_RCF = 7
    
    filter_text += '309h -> {}\n'.format(S_RCF)
    filter_text += '30Ah -> {}\n'.format(int(M_RCF-1))

    Offset = 0
    filter_text += '30Bh -> {}\n'.format(Offset)

    ntaps = int(M_RCF)
    filter_text += '30Ch -> {}\n'.format(ntaps-1)
    filter_text += '30Dh -> 0\n'

    fsamp = fclock/(M_CIC2*M_CIC5*M_RCF)
    
    tap = int(2.0*((2**19)-1)/(ntaps*OL_CIC5))
    for p in range(0, ntaps):
        filter_text += ' {} -> {}\n'.format(p, int(math.ceil(tap)))#filter_text += ' {} -> {}\n'.format(p, int(math.ceil(hn)))
    
    filter_text += 'RCF Gain -> .999996185302734\n'
    filter_text += 'Chip Restarted:\n'
    filter_text += '300h -> 1\n'
    filter_text += '300h -> 0'

    filter_name = '{}_{}MHz_clock{}MHz_F{}MHz_{}_{}_{}.jars'.format(
        abs(fch),
        int((abs(fch)-abs(int(fch)))*1000),
        fclock,
        round(fsamp,3),
        M_CIC2,
        M_CIC5,
        M_RCF
    )
    
    #jars_file = open(os.path.join(folder_name, filter_name), 'wb')
    #jars_file.write(filter_text)
    #jars_file.close()
    print 'Filter .jars has been created'
    racp_text += 'JARS_FILTER={}\n'.format(os.path.join(folder_name, filter_name))
    racp_text += 'MARK WIDTH=2\n'
    racp_text += 'GENERATE OWN SAMPLING WINDOW=NO\n'

    if jars['save_data']:
        racp_text += 'SAVE DATA=YES\n'
    else:
        racp_text += 'SAVE DATA=NO\n'

    racp_text += 'RC_STOP_SEQUENCE=255,0\n'
    racp_text += 'RC_START_SEQUENCE=255,24\n'

    #racp_file.write(racp_text)
    #racp_file.close()

    return racp_text, filter_text