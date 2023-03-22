from django.db import models
from apps.main.models import Configuration , User
from django.urls import reverse
from celery.execute import send_task
from datetime import datetime
import ast
import socket
import json
import requests
import struct
import os, sys, time

from .mqtt import client as mqtt_client
from radarsys.socketconfig import sio as sio
import json

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

status_default = '0000000000000000000000000000000000000000000000000000000000000000'
default_messages = {}

for i in range(1,65):
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
    active_beam     = models.PositiveSmallIntegerField(verbose_name='Active Beam', default=0)
    module_status   = models.CharField(verbose_name='Module Status', max_length=10000, default=status_default)
    operation_mode  = models.PositiveSmallIntegerField(verbose_name='Operation Mode', choices=OPERATION_MODES, default = 0)
    operation_value = models.FloatField(verbose_name='Periodic (seconds)', default="10", null=True, blank=True)
    module_messages = models.CharField(verbose_name='Modules Messages', max_length=10000, default=json.dumps(default_messages))

    class Meta:
        db_table = 'abs_configurations'

    def get_absolute_url_plot(self):
        return reverse('url_plot_abs_patterns', args=[str(self.id)])


    def parms_to_dict(self):

        parameters = {}

        parameters['device_id'] = self.device.id
        parameters['label']      = self.label
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

        self.label = parameters['label']

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
        new_beams = ABSBeam.objects.filter(abs_conf=self)
        self.active_beam = new_beams[0].id
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
        self.active_beam = 0
        self.device.save()
        self.message = 'ABS has been stopped.'
        self.save()

        return True

    def stop_device_mqtt(self):

        self.device.status = 2
        self.active_beam = 0
        # conf_active = None
        # conf_active.save()
        self.device.save()
        self.message = 'ABS has been stopped.'
        self.save()

        mqtt_client.publish(os.environ.get('TOPIC_ABS', 'abs/beams'),"STOP")

        return True

    def write_device(self):

        """
        This function sends the beams list to every abs module.
        It needs 'module_conf' function
        """
        
        beams  = ABSBeam.objects.filter(abs_conf=self)
        nbeams = len(beams)
        
        # Se manda a cero RC para poder realizar cambio de beam
        if self.experiment is None:
            confs = []
        else:
            confs = Configuration.objects.filter(experiment = self.experiment).filter(type=0)
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

        '''
        if self.connected_modules() == 0 :
            print("No encuentra modulos")
            self.message = "No ABS Module detected."
            return False
        '''
        #-------------Write each abs module-----------

        if beams:
            block_id = 0
            message = 'SNDF{:03d}{:02d}{:02d}'.format(nbeams, nbeams, block_id)
            for i, status in enumerate(self.module_status):
                message += ''.join([fromBinary2Char(beam.module_6bits(i)) for beam in beams])
            status = ['0'] * 64
            n = 0
            sock = self.send_multicast(message)

            while True:
            #for i in range(32):
                try:
                    data, address = sock.recvfrom(1024)
                    print (address, data)
                    data = data.decode("utf-8")
                    if data == '1':
                        status[int(address[0][10:])-1] = '3'
                        #print (int(address[0][10:])-1)
                    elif data == '0':
                        status[int(address[0][10:])-1] = '1'
                except socket.timeout:
                    print('Timeout')
                    break
                except Exception as e:
                    print ('Error {}'.format(e))
                    n += 1
            sock.close()
        else:
            self.message = "ABS Configuration does not have beams"
            # print('No beams')
            #Start DDS-RC-JARS
            if confdds:
                confdds.start_device()
            if confrc:
                #print confrc
                confrc.start_device()
            if confjars:
                confjars.start_device()
            return False

        if n == 64:
            self.message = "Could not write ABS Modules"
            self.device.status = 0
            self.module_status = ''.join(status)
            self.save()
            # print('Could not write ABS')
            #Start DDS-RC-JARS
            if confdds:
                confdds.start_device()
            if confrc:
                #print confrc
                confrc.start_device()
            if confjars:
                confjars.start_device()
            return False
        else:
            self.message = "ABS Beams List have been sent to ABS Modules"
            print('ABS beams list sent')
            self.active_beam = beams[0].pk

        #Start DDS-RC-JARS
        if confdds:
            confdds.start_device()
        if confrc:
            #print confrc
            confrc.start_device()
        if confjars:
            confjars.start_device()

        # print('Inicia intento de salvar device.status')
        self.device.status = 3
        self.module_status = ''.join(status)
        #print(status)
        self.save()
        # print('Estatus salvado')
        conf_active, __ = ABSActive.objects.get_or_create(pk=1)
        conf_active.conf = self
        conf_active.save()
        return True
    

# DEV_STATES = (
#                  (0, 'No connected'),
#                  (1, 'Connected'),
#                  (2, 'Configured'),
#                  (3, 'Running'),
#                  (4, 'Unknown'),
#                  (5, 'Busy')
#              )
    
    def write_device_mqtt(self):

        if self.experiment is None:
            confs = []
        else:
            confs = Configuration.objects.filter(experiment = self.experiment).filter(type=0)
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

        apuntes_up_down=''
        beams  = ABSBeam.objects.filter(abs_conf=self)

        inicializacion="{\"beams\":["
        finalizacion="]}"

        for beam in beams:
            beam.antenna=beam.antenna[1:]
            info="{\"id\":"+str(beam.id)+","+beam.antenna + ","
            apuntes_up_down=apuntes_up_down+info
        
        apuntes_up_down=apuntes_up_down[:len(apuntes_up_down)-1]
        apuntes_up_down=inicializacion+ apuntes_up_down+finalizacion
        mqtt_client.publish(os.environ.get('TOPIC_ABS', 'abs/beams'),apuntes_up_down)

        self.active_beam = beams[0].pk

        #Start DDS-RC-JARS
        if confdds:
            confdds.start_device()
        if confrc:
            #print confrc
            confrc.start_device()
        if confjars:
            confjars.start_device()

        self.device.status = 3
        self.save()

        conf_active, __ = ABSActive.objects.get_or_create(pk=1)
        conf_active.conf = self
        conf_active.save()
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


    def connected_modules(self):
        """
        This function returns the number of connected abs-modules without updating.
        """
        num = 0
        print(self.module_status)
        for i, status in  enumerate(self.module_status):
            if status != '0':
                num += 1
                #print('status {}:{}'.format(i+1, status))
        return num

    def send_multicast(self, message):
        #print("Send multicast")
        multicast_group = ('224.3.29.71', 10000)
        # Create the datagram socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1)
        local_ip = os.environ.get('LOCAL_IP', '0.0.0.0')
        local_ip = '0.0.0.0'
        print("He llegado a IP local")
        
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(local_ip))
        sock.sendto(message.encode(), multicast_group)
        print('Sending ' + message)
        return sock

    def status_device(self):
        """
        This function returns the status of all abs-modules as one.
        If at least one module is connected, its answer is "1"
        """
        print ('Status device')
        print (self.active_beam)
        beams = ABSBeam.objects.filter(abs_conf=self)
        #print beams[self.active_beam-1].module_6bits(0)
        active = ABSActive.objects.get(pk=1)
        if active.conf != self:
            self.message = 'La configuracion actual es la del siguiente enlace %s.' % active.conf.get_absolute_url()
            self.message +=  "\n"
            self.message += 'Se debe realizar un write en esta configuracion para luego obtener un status valido.'

            return False

        sock = self.send_multicast('MNTR')
        # print("Estoy en status_deice",flush=True)

        n = 0
        status = ['0'] * 64

        while True:
        #for i in range(32):
            #if True:
            try:
                print("Recibiendo")
                address = None
                data, address = sock.recvfrom(2)
                print (address, data)
                print("!!!!")
                data = data.decode()
                aux_mon = "1"
                aux_expected = aux_mon
                if(len(data)==2):
                    print ("data[1]: ")
                    print (data[1])
                    aux_mon = fromChar2Binary(data[1])
                    print (aux_mon)
                    aux_i = (str(address[0]).split('.'))[3]
                    print (aux_i)
                    print ('Active beam')
                    beam_active = ABSBeam.objects.get(pk=self.active_beam)
                    print (beam_active)
                    aux_expected = beam_active.module_6bits(int(aux_i)-1)
                    print (aux_expected)

                print ("data[0]: ")
                print (data[0])

                if data[0] == '1':
                    status[int(address[0][10:])-1] = '3'
                    if aux_mon == aux_expected:
                        print ('Es igual')
                    else:
                        print ('Es diferente')
                        status[int(address[0][10:])-1] = '2'

                elif data[0] == '0':
                    status[int(address[0][10:])-1] = '1'
                n += 1
                print('Module: {} connected'.format(address))
            except socket.timeout:
                print('Timeout')
                break
            except:
                print('Module: {} error'.format(address))
                pass

        sock.close()

        if n > 0:
            self.message = 'ABS modules Status have been updated.'
            self.device.status = 1
        else:
            self.device.status = 0
            self.message = 'No ABS module is connected.'
        self.module_status = ''.join(status)
        self.save()

        return self.device.status


    def send_beam(self, beam_pos):
        """
        This function connects to a multicast group and sends the beam number
        to all abs modules.
        """
        print ('Send beam')
        print (self.active_beam)
        beams = ABSBeam.objects.filter(abs_conf=self)
        #print beams[self.active_beam-1].module_6bits(0)
        active = ABSActive.objects.get(pk=1)
        if active.conf != self:
            self.message = 'La configuracion actual es la del siguiente enlace %s.' % active.conf.get_absolute_url()
            self.message +=  "\n"
            self.message += 'Se debe realizar un write en esta configuracion para luego obtener un status valido.'

            return False

        # Se manda a cero RC para poder realizar cambio de beam
        if self.experiment is None:
            confs = []
        else:
            confs = Configuration.objects.filter(experiment = self.experiment).filter(type=0)
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
        status = ['0'] * 64
        message = 'CHGB{}'.format(beam_pos)
        sock = self.send_multicast(message)
        print("Estoy en send_beam ",flush=True)
        while True:
        #for i in range(32):
            try:
                data, address = sock.recvfrom(1024)
                print (address, data)
                data = data.decode()
                if data == '1':
                    status[int(address[0][10:])-1] = '3'
                elif data == '0':
                    status[int(address[0][10:])-1] = '1'
            except socket.timeout:
                print('Timeout')
                break
            except  Exception as e:
                print ('Error {}'.format(e))
                pass

        sock.close()

        #Start DDS-RC-JARS
        if confdds:
            confdds.start_device()
        if confrc:
            #print confrc
            confrc.start_device()
        if confjars:
            confjars.start_device()

        self.message = "ABS Beam has been changed"
        self.module_status = ''.join(status)
        self.save()
        return True

    def change_beam_mqtt(self, beam_pos):
        """
        This function connects send through mqtt the order of change_beam (id of beam).
        """
        print ('Change beam MQTT')
        print (self.active_beam)
        beams = ABSBeam.objects.filter(abs_conf=self)
        #print beams[self.active_beam-1].module_6bits(0)
        active = ABSActive.objects.get(pk=1)
        if active.conf != self:
            self.message = 'La configuracion actual es la del siguiente enlace %s.' % active.conf.get_absolute_mqtt_url()
            self.message +=  "\n"
            self.message += 'Se debe realizar un write en esta configuracion para luego obtener un status valido.'

            return False

        # Se manda a cero RC para poder realizar cambio de beam
        if self.experiment is None:
            confs = []
        else:
            confs = Configuration.objects.filter(experiment = self.experiment).filter(type=0)
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

        mqtt_client.publish('abs/change_beam',str(beam_pos))


        #Start DDS-RC-JARS
        if confdds:
            confdds.start_device()
        if confrc:
            confrc.start_device()
        if confjars:
            confjars.start_device()

        self.message = "ABS Beam has been changed"
        self.save()
        return True

    def get_absolute_url_import(self):
        return reverse('url_import_abs_conf', args=[str(self.id)])

class ABSActive(models.Model):
    conf = models.ForeignKey(ABSConfiguration, null=True, verbose_name='ABS Configuration', on_delete=models.CASCADE)

    class Meta:
        db_table = 'abs_absactive'

class ABSBeam(models.Model):

    name         = models.CharField(max_length=60, default='Beam')
    antenna      = models.CharField(verbose_name='Antenna', max_length=1000, default=antenna_default)
    abs_conf     = models.ForeignKey('ABSConfiguration', null=True,
    verbose_name='ABS Configuration', on_delete=models.CASCADE)
    tx           = models.CharField(verbose_name='Tx', max_length=1000, default=tx_default)
    rx           = models.CharField(verbose_name='Rx', max_length=1000, default=rx_default)
    s_time       = models.TimeField(verbose_name='Star Time', default='00:00:00')
    e_time       = models.TimeField(verbose_name='End Time', default='23:59:59')
    ues          = models.CharField(verbose_name='Ues', max_length=100, default=ues_default)
    only_rx      = models.CharField(verbose_name='Only RX', max_length=40, default=onlyrx_default)

    class Meta:
        db_table = 'abs_beams'

    def __unicode__(self):
        return u'%s' % (self.name)

    def parms_to_dict(self):

        parameters = {}
        parameters['name']          = self.name
        parameters['antenna']       = ast.literal_eval(self.antenna)
        parameters['abs_conf']      = self.abs_conf.name
        parameters['tx']            = ast.literal_eval(self.tx)
        parameters['rx']            = ast.literal_eval(self.rx)
        parameters['s_time']        = self.s_time.strftime("%H:%M:%S")
        parameters['e_time']        = self.e_time.strftime("%H:%M:%S")
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
        module += 1
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
