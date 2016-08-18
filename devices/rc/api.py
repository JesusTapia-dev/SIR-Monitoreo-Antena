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
CMD_DISABLE         =0X02
CMD_ECHO            =0XFE

RC_CMD_RESET        =0X10
RC_CMD_WRITE        =0x50
RC_CMD_READ         =0x8000
RC_CMD_ENABLE       =0X24
RC_CMD_DISABLE      =0X00

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
def enable():
    
    cmd = RC_CMD_ENABLE
    payload = chr(0x01)
    
    return cmd, payload

@eth_device(ID_CLASS)
def disable():
    
    cmd = RC_CMD_DISABLE
    payload = chr(0x00)
    
    return cmd, payload

@eth_device(ID_CLASS)
def read_all_device():
    
    payload = ""
    
    return RC_CMD_READ, payload

@eth_device(ID_CLASS)
def write_all_device(payload):
    
    return RC_CMD_WRITE, payload

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
    
    payload = write_ram_memory(parms['pulses'], parms['delays'])
    
    answer = write_all_device(ip, port, payload)
    
    return answer

def __get_low_byte(valor):
   
    return ord(valor & 0x00FF)
   
def __get_high_byte(valor):
   
    return ord((valor & 0xFF00) >> 8)


def write_ram_memory(vector_valores, vector_tiempos):

    l1 = len(vector_valores)
    l2 = len(vector_tiempos)
    
    cad = ""
    
    for i in range(l1):
        cad += ord(84) + __get_low_byte(vector_valores[i]) + ord(85) + __get_high_byte(vector_valores[i]) + \
             ord(84) + __get_low_byte(vector_tiempos[i]) + ord(85) + __get_high_byte(vector_tiempos[i])
    
    return cad

if __name__ == '__main__':
    ip = "10.10.20.150"
    port = 2000
    
    print status(ip, port)
    print read_config(ip, port)