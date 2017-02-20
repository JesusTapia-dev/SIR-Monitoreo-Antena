from django.db import models
from apps.main.models import Configuration
from django.core.urlresolvers import reverse
# Create your models here.
from celery.execute import send_task
from datetime import datetime
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
default_messages = {}
default_modulemode = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0,
                      "11": 0, "12": 0, "13": 0, "14": 0, "15": 0, "16": 0, "17": 0, "18": 0, "19": 0, "20": 0,
                      "21": 0, "22": 0, "23": 0, "24": 0, "25": 0, "26": 0, "27": 0, "28": 0, "29": 0, "30": 0,
                      "31": 0, "32": 0, "33": 0, "34": 0, "35": 0, "36": 0, "37": 0, "38": 0, "39": 0, "40": 0,
                      "41": 0, "42": 0, "43": 0, "44": 0, "45": 0, "46": 0, "47": 0, "48": 0, "49": 0, "50": 0,
                      "51": 0, "52": 0, "53": 0, "54": 0, "55": 0, "56": 0, "57": 0, "58": 0, "59": 0, "60": 0,
                      "61": 0, "62": 0, "63": 0, "64": 0}  # 0 :  Socket  //  1: API Rest

for i in range(1,65):
    conf_default[str(i)] = ""
    status_default[str(i)] = 0
    default_messages[str(i)] = "Module "+str(i)


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

def up_conv_value(bits):

    if bits == "000": value=1.0
    if bits == "001": value=2.0
    if bits == "010": value=3.0
    if bits == "011": value=0.0
    if bits == "100": value=0.5
    if bits == "101": value=1.5
    if bits == "110": value=2.5
    if bits == "111": value=3.5

    return value

def down_conv_value(bits):

    if bits == "000": value=1.0
    if bits == "001": value=2.0
    if bits == "010": value=3.0
    if bits == "011": value=0.0
    if bits == "100": value=0.5
    if bits == "101": value=1.5
    if bits == "110": value=2.5
    if bits == "111": value=3.5

    return value

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
    module_messages = models.CharField(verbose_name='Modules Messages', max_length=10000, default=json.dumps(default_messages))
    module_mode     = models.CharField(verbose_name='Modules Mode', max_length=10000, default=json.dumps(default_modulemode))

    class Meta:
        db_table = 'abs_configurations'

    def get_absolute_url_plot(self):
        return reverse('url_plot_abs_patterns', args=[str(self.id)])


    def parms_to_dict(self):

        parameters = {}

        parameters['device_id'] = self.device.id
        parameters['name']      = self.name
        parameters['device_type']      = self.device.device_type.name
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

        #-----For Active Beam-----
        active_beam = json.loads(self.active_beam)
        new_beams = ABSBeam.objects.filter(abs_conf=self)
        active_beam['active_beam'] = new_beams[0].id

        self.active_beam = json.dumps(active_beam)
        self.save()
        #-----For Active Beam-----
        #-----For Device Status---
        self.device.status = 3
        self.device.save()
        #-----For Device Status---

        return self


    def start_device(self):

        if self.device.status == 3:

            try:
                #self.write_device()
                send_task('task_change_beam', [self.id],)
                self.message = 'ABS running'

            except Exception as e:
                self.message = str(e)
                return False

            return True

        else:
            self.message = 'Please, select Write ABS Device first.'
            return False


    def stop_device(self):

        self.device.status = 2
        self.device.save()
        self.message = 'ABS has been stopped.'
        self.save()

        return True

    def monitoring_device(self):

        monitoreo_tx = 'JROABSClnt_01CeCnMod000000MNTR10'
        beam_tx = 'JROABSCeCnModCnMod01000001CHGB10'

        beam_pos = 1
        module_address = ('192.168.1.63', 5500)

        message_tx = monitoreo_tx
        # Create the datagram socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(module_address)

        sock.send(message_tx)
        t = sock.recv(1024)
        print 'Respuesta: \n',t
        sock.close()
        sock = None

        return True


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

        #header = 'JROABSCeCnModCnMod01000108SNDFexperimento1.ab1'
        #module = 'ABS_'+str(module_num)
        bs  = '' #{}
        i=1

        for beam in beams:
            #bs[i] = fromBinary2Char(beam.module_6bits(module_num))
            bs = bs + fromBinary2Char(beam.module_6bits(module_num))
            i=i+1

        beams = bs

        parameters = {}
        parameters['beams']  = beams #json.dumps(beams)
        print parameters
        answer = ''

        try:
            #r_write = requests.post(write_route, parameters, timeout=0.5)
            r_write = requests.post(write_route, json = parameters, timeout=0.5)
            answer  = r_write.json()
            #self.message = answer['message']
        except:
            #self.message = "Could not write ABS parameters"
            return False

        return answer



    def write_device(self):

        """
        This function sends the beams list to every abs module.
        It needs 'module_conf' function
        """

        beams = ABSBeam.objects.filter(abs_conf=self)
        connected_modules = ast.literal_eval(self.module_status)
        suma_connected_modules = 0

        for c in connected_modules:
            suma_connected_modules = suma_connected_modules+connected_modules[c]
        if not suma_connected_modules > 0 :
            self.message = "No ABS Module detected."
            return False

        #-------------Write each abs module-----------
        if beams:
            beams_status = ast.literal_eval(self.module_status)
            disconnected_modules = 0
            for i in range(1,65): #(62,65)
                #--------------JUEVES-------------
                if beams_status[str(i)] != 0:
                    try:
                        answer = self.module_conf(i,beams)
                        if answer:
                            if answer['status']:
                                beams_status[str(i)] = 3
                                print snswer

                    except:
                        beams_status[str(i)] = 1

                        pass
                else:
                    disconnected_modules += 1

        else:
            self.message = "ABS Configuration does not have beams"
            return False

        #self.device.status = 1
        ##
        #-------------Jueves-------------
        if disconnected_modules == 64:
            self.message = "Could not write ABS Modules"
            self.device.status = 0
            return False
        else:
            self.message = "ABS Beams List have been sent to ABS Modules"
            beams[0].set_as_activebeam()

        self.device.status = 3
        self.module_status = json.dumps(beams_status)



        self.save()
        return True




    def read_module(self, module):

        """
        Read out-bits (up-down) of 1 abs module NOT for Configuration
        """

        ip_address  = self.device.ip_address
        ip_address  = ip_address.split('.')
        module_seq  = (ip_address[0],ip_address[1],ip_address[2])
        dot         = '.'
        module_ip   = dot.join(module_seq)+'.'+str(module)
        module_port = self.device.port_address
        read_route = 'http://'+module_ip+':'+str(module_port)+'/read'

        module_status = json.loads(self.module_status)
        print(read_route)

        module_bits = ''

        try:
            r_read      = requests.get(read_route, timeout=0.5)
            answer      = r_read.json()
            module_bits = answer['allbits']
        except:
            return {}

        return module_bits

    def read_device(self):

        parms = {}
        # Reads active modules.
        module_status = json.loads(self.module_status)
        total = 0
        for status in module_status:
            if module_status[status] != 0:
                module_bits = self.read_module(int(status))
                bits={}
                if module_bits:
                    bits = (str(module_bits['um2']) + str(module_bits['um1']) + str(module_bits['um0']) +
                            str(module_bits['dm2']) + str(module_bits['dm1']) + str(module_bits['dm0']) )
                    parms[str(status)] = bits

                total +=1

        if total==0:
            self.message = "No ABS Module detected. Please select 'Status'."
            return False



        self.message = "ABS Modules have been read"
        #monitoreo_tx = JROABSClnt_01CeCnMod000000MNTR10
        return parms


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
        module_messages = json.loads(self.module_messages)

        for i in range(1,65):
            module_ip   = dot.join(module_seq)+'.'+str(i)
            print module_ip

            route = 'http://'+module_ip+':'+str(module_port)+'/status'

            try:
                r = requests.get(route, timeout=0.6)#, timeout=0.7)
                answer = r.json()
                modules_status[str(i)] = answer['status']
                module_messages[str(i)] = answer['message']
            except:
                modules_status[str(i)] = 0
                pass


        self.module_status   = json.dumps(modules_status)
        self.module_messages = json.dumps(module_messages)
        self.save()

        return


    def connected_modules(self):
        """
        This function returns the number of connected abs-modules without updating.
        """
        modules_status = json.loads(self.module_status)
        num = 0
        for status in modules_status:
            if modules_status[status] != 0:
                num += 1

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
        ip_address  = self.device.ip_address
        ip_address  = ip_address.split('.')
        module_seq  = (ip_address[0],ip_address[1],ip_address[2])
        dot         = '.'
        module_ip   = dot.join(module_seq)+'.'+str(module)
        module_port = self.device.port_address
        write_route = 'http://'+module_ip+':'+str(module_port)+'/write'

        #print write_route

        #header = 'JROABSCeCnModCnMod01000108SNDFexperimento1.ab1'
        #module = 'ABS_'+str(module)
        beams  = '!`*3<ENW'#{1: '001000', 2: '010001', 3: '010010', 4: '000011', 5: '101100', 6: '101101',
                 # 7: '110110', 8: '111111', 9: '000000', 10: '001001', 11: '010010', 12: '011011'}

        #parameters['header'] = header
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


    def write_module_socket(self, module):
        """
        This function sends beams list to one abs-module to TCP_Control_Module using sockets
        """

        ip_address  = self.device.ip_address
        ip_address  = ip_address.split('.')
        module_seq  = (ip_address[0],ip_address[1],ip_address[2])
        dot         = '.'
        module_ip   = dot.join(module_seq)+'.'+str(module)
        module_port = self.device.port_address

        header = 'JROABSCeCnModCnMod01000108SNDFexperimento1.ab1'
        abs_module = 'ABS_'+str(module)

        beams      = self.get_beams()
        beams_text = ''
        for beam in beams:
            modules_conf=json.loads(beam.modules_conf)
            beams_text = beams_text + modules_conf[str(module)] + '\n'

        message_tx = header + '\n' + abs_module + '\n' + beams_text + '0'
        print "Send: ", message_tx

        # Create the datagram socket
        module_address = (module_ip, 5500)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(module_address)
            sock.send(message_tx)
            t = sock.recv(1024)
            print 'Respuesta: \n',t

        except Exception as e:
            print str(e)
            sock.close()
            sock = None
            return False

        sock.close()
        sock = None

        return True

    def write_device_socket(self):
        """
        This function sends beams list to every connected abs-module to TCP_Control_Module using sockets
        """
        module_mode   = json.loads(self.module_mode)
        module_status = json.loads(self.module_status)

        for i in range(1,65):
            if module_mode[str(i)] == 0 and module_status[str(i)] == 1: # 0: Sockets + Cserver & 1: Connected
                try:
                    self.write_module_socket(i)
                except Exception as e:
                    print 'Error ABS '+str(i)+': '+str(e)

        return True


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

        # Se manda a cero RC para poder realizar cambio de beam
        confs = Configuration.objects.filter(experiment = self.experiment)
        confdds  = ''
        confjars = ''
        confrc   = ''

        #TO STOP DEVICES: DDS-JARS-RC
        for i in range(0,len(confs)):
            if i==0:
                for conf in confs:
                    if conf.device.device_type.name == 'dds':
                        confdds = conf
                        confdds.stop_device()
                        break
            if i==1:
                for conf in confs:
                    if conf.device.device_type.name == 'jars':
                        confjars = conf
                        confjars.stop_device()
                        break
            if i==2:
                for conf in confs:
                    if conf.device.device_type.name == 'rc':
                        confrc = conf
                        confrc.stop_device()
                        break

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

        try:
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        except Exception as e:
            self.message = str(e)
            print str(e)
            sock.close()
            sock = None
            return False

        #print 'sending acknowledgement to all: \n' + message_tx
        try:
             sock.sendto(message_tx, (multicast_group, 10000))
        except Exception as e:
             self.message = str(e)
             print str(e)
             sock.close()
             sock = None
             return False
        sock.close()
        sock = None

        #Start DDS-RC-JARS
        if confdds:
            confdds.start_device()
        if confrc:
            #print confrc
            confrc.start_device()
        if confjars:
            confjars.start_device()

        self.message = "ABS Beam has been changed"

        return True

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
