'''
Created on Nov 25, 2015

@author: Miguel Urco

eth_device decorator is used to implement an api to ethernet devices.
When eth_device decorator is used it adds two parameters to any function (ip and port)

#Definition of a function using eth_device decorator

@eth_device(ID_CLASS)
def enable_acq(message)
    cmd = "xxxxx"
    payload = message

    return cmd, payload

#How to call this function:
answer = enable_acq(ip, port, message)

'''
import sys
import struct
import json

from devices.jro_device import eth_device, IdClass

ID_CLASS = IdClass["jars"]

CMD_RESET = 0X01
CMD_CHANGEIP = 0X03
#Add other commands
CMD_CONFIGURE = 0X10
CMD_STATUS = 0X11
CMD_SET_EXEPATH = 0X12
CMD_ECHO = 0XFE
CMD_READ = 0X08
CMD_STOP = 0X09

@eth_device(ID_CLASS)
def reset():

    cmd = CMD_RESET
    payload = ''

    return cmd, payload

@eth_device(ID_CLASS)
def stop():

    cmd = CMD_STOP
    payload = ''

    return cmd, payload

@eth_device(ID_CLASS)
def echo(message):

    cmd = CMD_ECHO
    payload = message

    return cmd, payload

@eth_device(ID_CLASS)
def configure(conf):

    cmd = CMD_CONFIGURE
    payload = conf

    return cmd, payload

@eth_device(ID_CLASS)
def status():

    cmd = CMD_STATUS
    payload = ''

    return cmd, payload

@eth_device(ID_CLASS)
def read():

    cmd = CMD_READ
    payload = ''

    return cmd, payload

@eth_device(ID_CLASS)
def set_exepath(path):

    cmd = CMD_SET_EXEPATH
    payload = path

    return cmd, payload

#--To take .json file from computer:
#with open('/home/fquino/Downloads/Experiment.json') as data_file:
#    data = json.load(data_file)

#    data['configurations']['dds']=''
#    data['configurations']['rc']['pulses']=''
#    data['configurations']['rc']['delays']=''
    
    #data = json.dumps(data)
#-----------------------------------

#print reset('10.10.10.100', 10000)
#print echo('10.10.10.95', 10000, 'Hola JARS :)')

#json_data = json.dumps({'name':'archivo1','variable':9})
#print configure('10.10.10.95', 10000, data)
#print configure('10.10.10.100', 10000, '')
#print status('10.10.10.100', 10000)
