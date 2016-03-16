'''
Created on Dec 2, 2014

@author: Miguel Urco

eth_device decorator is used to implement an api to ethernet devices.
When eth_device decorator is used it adds two parameters to any function (ip and port)

#Definition

@eth_device
def enable_rf()
    cmd = "xxxxx"
    payload = "xxxxxx"
    
    return cmd, payload
    
#How to call this function:
answer = enable_rf(ip, port)

'''
import data

from devices.jro_device import eth_device, IdClass

ID_CLASS = IdClass["rc"]

CMD_RESET           =0X01
CMD_ENABLE          =0X02
CMD_CHANGEIP        =0X03
CMD_STATUS          =0X04
CMD_ECHO            =0XFE

DDS_CMD_RESET       =0X10
DDS_CMD_ENABLE_RF   =0x11
# DDS_CMD_MULTIPLIER  =0X12
# DDS_CMD_MODE        =0x13
# DDS_CMD_FREQUENCY_A  =0X14
# DDS_CMD_FREQUENCY_B  =0x15
# DDS_CMD_PHASE_A      =0X16
# DDS_CMD_PHASE_B      =0x17
# DDS_CMD_AMPLITUDE_1  =0X19      #Se han invertido la posicion de los canales
# DDS_CMD_AMPLITUDE_2  =0x18      #en el PCB

DDS_CMD_WRITE        =0x50
DDS_CMD_READ        =0x8000

@eth_device(ID_CLASS)
def reset():
    
    cmd = CMD_RESET
    payload = ""
    
    return cmd, payload

@eth_device(ID_CLASS)
def change_ip(ip, mask="255.255.255.0", gateway="0.0.0.0"):
    
    cmd = CMD_CHANGEIP
    payload = ip + '/' + mask + '/' + gateway
    
    return cmd, payload

@eth_device(ID_CLASS)
def status():
    
    cmd = CMD_STATUS
    payload = ""
    
    return cmd, payload

@eth_device(ID_CLASS)
def echo():
    
    cmd = CMD_ECHO
    payload = ""
    
    return cmd, payload

@eth_device(ID_CLASS)
def read_all_device():
    
    payload = ""
    
    return DDS_CMD_READ, payload

@eth_device(ID_CLASS)
def write_all_device(payload):
    
    return DDS_CMD_WRITE, payload

def read_config(ip, port):
    """
    Output:
        parms   : Dictionary with keys
    
    """
    payload = read_all_device(ip, port)
    
    return data.rc_str_to_dict(payload)
    
def write_config(ip, port, parms):
    """
    Input:
        ip      :
        port    :
        parms   : Dictionary with keys
    
    """
    
    payload = data.dict_to_rc_str(parms)
    
    answer = write_all_device(ip, port, payload)
    
    return answer

if __name__ == '__main__':
    ip = "10.10.20.150"
    port = 2000
    
    print status(ip, port)
    print read_config(ip, port)