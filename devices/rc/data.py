'''
Created on Feb 15, 2016

@author: Miguel Urco
'''
import struct

def rc_str_to_dict(registers):
    
    parms = {'clock' : 10
            }
    
    return parms

def dict_to_rc_str(parms):
    """
    Input:
        parms   : Dictionary with keys
    """
    
    my_dict = {'clock' : 10
            }
    
    registers = ord(my_dict['clock'])
    
    return registers