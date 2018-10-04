'''
Created on Jan 5, 2016

@author: Juan C. Espinoza

'''

import os
import math
import json
import requests
import time

from threading import Thread
from subprocess import Popen, PIPE
from collections import deque
from datetime import datetime, timedelta

from flask import Flask, jsonify, request, send_file

PATH = 'F:\SIR_DATA'
EXE = 'C:\JROAdquisicion\src\JROAcquisitionSoftware\Release\JROAcquisitionSoftware.exe'
IPHOST='10.10.10.165'
OPT = '--jars' #'--cbsim'
PROC = False
OUT = None
LOGGING = False
global EXPNAME

DECODE_TYPE = {1:'DECODING_TIME_DOMAIN',2:'DECODING_FREQ_DOMAIN',3:'DECODING_INV_FREQ_DOMAIN'}

app = Flask(__name__)

class StdoutReader(object):
    '''
    Class to manage stdout of JARS acquisition program
    '''

    def __init__(self, stream, name):
        '''
        stream: the stream to read from.
                Usually a process' stdout or stderr.
        '''

        self._s = stream
        self._q = deque()
        self._f = open(os.path.join(PATH, name, 'Restarting Report.txt'), 'ab')
        if LOGGING:
            self._l = open(os.path.join(PATH, name, '{}.log'.format(name)), 'ab')

        def update_queue(stream, queue):
            '''
            Collect lines from 'stream' and put them in 'queue'.
            '''

            restart_dict = {}
            restart_num  = 0
            str_format   = '%Y-%m-%d %H:%M:%S'
            delta_time   = timedelta(0,120,0)
            while True:
                raw = stream.readline()
                line = raw.rstrip()
                now          = datetime.now()
                now_str      = now.strftime(str_format)
                restart_dict[str(restart_num)] = now_str
                max_num = 13
                if line:
                    queue.append(line)
                    if LOGGING:
                        self._l.write('{}'.format(raw))
                    print line
                    if 'Block' not in line:
                        self._f.write('{} at {}\n'.format(line,
                                                          datetime.now().ctime()))

                        restart_num = restart_num + 1
                        if restart_num > max_num:
                            date1 = datetime.strptime(restart_dict['1'], str_format)
                            date2 = datetime.strptime(restart_dict[str(max_num-1)], str_format)
                            if (date2 - date1) < delta_time:
                                print str(max_num)+' restarts en menos de 2min'#RESTART
                                restart_num  = 0
                                restart_dict = {}
                                restart()
                            else:
                                restart_num  = 0
                                restart_dict = {}
                                print 'NO'


        self._t = Thread(target=update_queue, args=(self._s, self._q))
        self._t.daemon = True
        self._t.start()

    def readline(self):
        '''
        Return last line output
        '''
        try:
            line = self._q.pop()
            self._q.clear()
            return line
        except IndexError:
            return None

    def save(self):
        '''
        Save logging files
        '''
        self._f.close()
        if LOGGING:
            self._l.close()

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
    global EXPNAME
    
    data = json.loads(json_data)
    exp_id = data['experiments']['allIds'][0]
    experiment = data['experiments']['byId'][exp_id]
    name = experiment['name']
    EXPNAME = name
    folder_name = os.path.join(PATH, name)
    print 'Experiment: ' + name + ' received...'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    if not os.path.exists(folder_name+'/DATA'):
        os.mkdir(folder_name+'/DATA')

	try:
        json_file = open(folder_name+'/'+name+'_jars.json', 'w')
    except:
        return 0, 'Error creating .json file'

    json_file.write(json_data)
    json_file.close()
		
    try:
        racp_file = open(folder_name+'/'+name+'_jars.racp', 'w')
    except:
        return 0, 'Error creating .racp file'

    conf_ids = data['configurations']['allIds']

    rcs = [pk for pk in conf_ids \
        if data['configurations']['byId'][pk]['device_type'] == 'rc']
    if len(rcs) == 1:
        rc_id = rcs[0]
        rc_mix_id = 0
    else:
        rcs = [pk for pk in conf_ids \
        if data['configurations']['byId'][pk]['device_type'] == 'rc' and data['configurations']['byId'][pk]['mix'] == True]
        rc_mix_id = rcs[0]
        mix_parameters = data['configurations']['byId'][rc_mix_id]['parameters'].split('-')
        rc_id = mix_parameters[0].split('|')[0] 
		
    jars_id = [pk for pk in conf_ids \
        if data['configurations']['byId'][pk]['device_type'] == 'jars'][0]
	
    rc = data['configurations']['byId'][rc_id]
    jars = data['configurations']['byId'][jars_id]

    if rc_mix_id <> 0:
        rc_mix = data['configurations']['byId'][rc_mix_id]
        mix_text = '*******Mixed Experiment*******************\n'
        mix_text += 'Number of Experiments={}\n'.format(len(mix_parameters))
        for i,param in enumerate(mix_parameters):
            pk, mode, op, delay, mask = param.split('|')
            mix_text += 'EXP({})={}\n'.format(i, data['configurations']['byId'][pk]['name'])
            mix_text += 'DELAY({})={}\n'.format(i, delay)
            mix_text += 'RELOJ={}\n'.format(int(data['configurations']['byId'][pk]['clock']))
            mix_text += 'MIXER MODE={}_FLAG\n'.format(op)
            mix_text += 'MIXER MASK={}\n'.format(mask)
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
    if rc_mix_id == 0:
        racp_text += 'IPP={}\n'.format(float(rc['ipp']))
        racp_text += 'NTX={}\n'.format(rc['ntx'])
    else:
        racp_text += 'IPP={}\n'.format(float(rc_mix['ipp']))
        racp_text += 'NTX={}\n'.format(rc_mix['ntx'])
    
    racp_text += 'TXA={}\n'.format(
        data['lines']['byId'][rc['lines'][1]]['params']['pulse_width']
    )
    if data['lines']['byId'][rc['lines'][2]]['line_type'] == 'tx':
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
    rangeTXA = data['lines']['byId'][rc['lines'][1]]['params']['range']
    if rangeTXA != '0':
        racp_text += 'Pulse selection_TXA={}\n'.format(rangeTXA)
    if data['lines']['byId'][rc['lines'][2]]['line_type'] == 'tx':
		rangeTXB = data['lines']['byId'][rc['lines'][2]]['params']['range']
		if rangeTXB != '0':
			racp_text += 'Pulse selection_TXB={}\n'.format(rangeTXB)
    for n in range(3, 6):
        racp_text += parse_line(n, data, rc['lines'])

    if data['lines']['byId'][rc['lines'][2]]['line_type'] == 'tx':
		taus = data['lines']['byId'][rc['lines'][2]]['params']['delays'].split(',')
		if taus != '0':
			racp_text += 'Number of Taus={}\n'.format(len(taus))
			for n, tau in enumerate(taus):
				racp_text += 'TAU({})={}\n'.format(n, tau)

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

        dum = jars['spectral']
        
        if dum.endswith(','):
            dum = dum[:-1]
        spectral = json.loads('[{}]'.format(dum))
        
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
    try:
        fclock = float(filter_parms['clock'])
        fch = float(filter_parms['fch'])
        m_dds = float(filter_parms['mult'])
        M_CIC2 = float(filter_parms['filter_2'])
        M_CIC5 = float(filter_parms['filter_5'])
        M_RCF = float(filter_parms['filter_fir'])
    except:
        fclock = eval(filter_parms['clock'])
        fch = eval(filter_parms['fch'])
        m_dds = eval(filter_parms['mult'])
        M_CIC2 = eval(filter_parms['filter_2'])
        M_CIC5 = eval(filter_parms['filter_5'])
        M_RCF = eval(filter_parms['filter_fir'])

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
    
    jars_file = open(os.path.join(folder_name, filter_name), 'wb')
    jars_file.write(filter_text)
    jars_file.close()
    racp_text += 'JARS_FILTER={}\n'.format(os.path.join(folder_name, filter_name))
    racp_text += 'MARK WIDTH=2\n'
    racp_text += 'GENERATE OWN SAMPLING WINDOW=NO\n'

    if jars['save_data']:
        racp_text += 'SAVE DATA=YES\n'
    else:
        racp_text += 'SAVE DATA=NO\n'

    racp_text += 'RC_STOP_SEQUENCE=255,0\n'
    racp_text += 'RC_START_SEQUENCE=255,24\n'

    racp_file.write(racp_text)
    racp_file.close()

    return 1, racp_file.name

@app.route('/status/')
def status():
    '''
    0 : Not configured/running
    3 : Running and acquiring data
    2 : Configured
    1 : Connected
    '''

    name = request.args.get('name', None)
    global EXPNAME
    EXPNAME = name

    if name is None:
        return jsonify({
            'status': 1,
            'message': 'JARS Connected, missing experiment'
        })
    else:
        racp_file = os.path.join(PATH, name, '{}_jars.racp'.format(name))

    if name and not os.path.exists(racp_file):
        return jsonify({
            'status': 1,
            'message': 'JARS not configured'
        })
    elif os.path.exists(racp_file) and hasattr(PROC, 'pid'):
        if PROC.poll() is None:
            status = 3
            msg = 'Process: PID={}, OUT={}'.format(
                PROC.pid,
                OUT.readline()
            )
        else:
            status = 2
            msg = 'JARS Configured'
    else:
        status = 2
        msg = 'JARS Configured'

    return jsonify({
        'status': status,
        'message': msg
    })

@app.route('/start/', methods=['POST'])
def start():
    '''
    '''

    global PROC
    global OUT
    global EXPNAME

    name = request.json['name']
    EXPNAME = name
    racp_file = os.path.join(PATH, name, '{}_jars.racp'.format(name))
    if hasattr(PROC, 'pid') and PROC.poll() is None:
        status = 3
        msg = 'JARS already running'
    elif os.path.exists(racp_file):
        PROC = Popen([EXE, '-rf', racp_file, OPT], stdout=PIPE)
        OUT = StdoutReader(PROC.stdout, name)
        status = 3
        msg = 'JARS starting ok'
    elif not os.path.exists(racp_file):
        status = 1
        msg = 'Experiment: {} not configured'.format(name)

    return jsonify({
        'status': status,
        'message': msg
    })

@app.route('/stop/', methods=['POST'])
def stop():
    '''
    '''

    global PROC

    if hasattr(PROC, 'pid'):
        if PROC.poll() is None:
            OUT.save()
            PROC.kill()
            status = 2
            msg = 'JARS stopped OK'
        else:
            status = 1
            msg = 'JARS not running'
    else:
        status = 1
        msg = 'JARS not running'

    return jsonify({
        'status': status,
        'message': msg
    })

@app.route('/write/', methods=['POST'])
def write():
    '''
    '''
    status = 1
    json_data = json.loads(request.json)
    conf_ids = json_data['configurations']['allIds']
    for pk in conf_ids:
        if json_data['configurations']['byId'][pk]['device_type'] == 'jars':
            data = json_data['configurations']['byId'][pk]['filter_parms']

    if request.json:
        try:
		    ret, racp = create_jarsfiles(request.json)
        except Exception as e:
            ret = 0
            msg = str(e)
    else:
        msg = 'Missing POST data'

    if ret == 1:
        status = 2
        msg = 'JARS configured OK'
    else:
        msg = ret

    return jsonify({
        'status': status,
        'message': msg
    })


def restart():
    '''
    '''

    global EXPNAME
    #ip_host = '10.10.10.99'
    port = 5000
    route_stop = 'http://'+IPHOST+':'+str(port)+'/stop/'
    stop = requests.post(route_stop, data={})
    print 'Restarting...'
    time.sleep(3)
    route_start = 'http://'+IPHOST+':'+str(port)+'/start/'
    start = requests.post(route_start, json={'name':EXPNAME})

    return

@app.route('/get_log/')
def get_log():
    '''
    This function sends Restarting Report.txt of the Experiment.
    '''

    name = request.args.get('name', None)
    global EXPNAME
    EXPNAME = name
    
    if name is None:
        return jsonify({
            'status': 1,
            'message': 'JARS Connected, missing experiment'
        })
    else:
        try:
            rr_file = os.path.join(PATH, name, 'Restarting Report.txt')
            return send_file(rr_file, attachment_filename='Restarting Report.txt')
        except Exception as e:
            return jsonify({
            'status': 1,
            'message': str(e)
            })    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
