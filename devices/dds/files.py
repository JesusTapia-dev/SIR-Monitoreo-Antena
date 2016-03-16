'''
Created on Feb 8, 2016

@author: Miguel Urco
'''

import string
import data

def read_dds_file(fp):
    """
    Function to extract the parameters from a text file with the next format: 
    
    Input:
    
        File with the next content:
        
        Phase Adjust Register 1
        -----------------------
        00000000
        00000000
        
        .....
        
        -----------------------
        Frequency Tuning Word 1
        -----------------------
        00110101
        01111111
        11111111
        11111111
        10100000
        00000000
    
    Output:
        Return configuration parameters for DDS: multiplier, frequency, phase, amplitude, etc.
    
    """
    
    registers = ""
    
    for this_line in fp:
        this_line = str.strip(this_line)
        
        if not str.isdigit(this_line):
            continue
        
        if len(this_line) != 8:
            continue
        
        registers += chr(string.atoi(this_line,2))
    
    parms = data.dds_str_to_dict(registers)
    
    return parms

def read_json_file(fp):
    
    kwargs = {}
    
    return kwargs

def write_dds_file(filename):
    pass

def write_json_file(filename):
    pass