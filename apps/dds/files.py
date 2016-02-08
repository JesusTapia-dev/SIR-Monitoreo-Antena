'''
Created on Feb 8, 2016

@author: Miguel Urco
'''

import string

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
    
    kwargs = {}
    dds_registers = []
    
    for this_line in fp:
        this_line = str.strip(this_line)
        
        if not str.isdigit(this_line):
            continue
        
        if len(this_line) != 8:
            continue
        
        dds_registers.append(string.atoi(this_line,2))
    
    if len(dds_registers) != 40:
        return kwargs
    
    kwargs['clock'] = 60.0
    
    kwargs['phase_bin'] = dds_registers[0]*(2**8) + dds_registers[1]
    kwargs['phase_mod_bin'] = dds_registers[2]*(2**8) + dds_registers[3]
    
    kwargs['frequency_bin'] = dds_registers[4]*(2**40) + dds_registers[5]*(2**32) + dds_registers[6]*(2**24) + dds_registers[7]*(2**16) + dds_registers[8]*(2**8) + dds_registers[9]
    kwargs['frequency_mod_bin'] = dds_registers[10]*(2**40) + dds_registers[11]*(2**32) + dds_registers[12]*(2**24) + dds_registers[13]*(2**16) + dds_registers[14]*(2**8) + dds_registers[15]
    
    kwargs['delta_frequency'] = dds_registers[16]*(2**40) + dds_registers[17]*(2**32) + dds_registers[18]*(2**24) + dds_registers[19]*(2**16) + dds_registers[20]*(2**8) + dds_registers[21]
    
    kwargs['update_clock'] = dds_registers[22]*(2**24) + dds_registers[23]*(2**16) + dds_registers[24]*(2**8) + dds_registers[25]
    
    kwargs['ramp_rate_clock'] = dds_registers[26]*(2**16) + dds_registers[27]*(2**8) + dds_registers[28]
    
    kwargs['control_register'] = dds_registers[29]*(2**24) + dds_registers[30]*(2**16) + dds_registers[31]*(2**8) + dds_registers[32]
    
    kwargs['multiplier'] = dds_registers[30] & 0x1F
    kwargs['modulation'] = (dds_registers[31] & 0x0E) >> 1
    kwargs['amplitude_enabled'] = (dds_registers[32] & 0x20) >> 5
    
    kwargs['amplitude_ch_A'] = (dds_registers[33]*(2**8) + dds_registers[34]) & 0x0FFF
    kwargs['amplitude_ch_B'] = (dds_registers[35]*(2**8) + dds_registers[36]) & 0x0FFF
    
    kwargs['amplitude_ramp_rate'] = dds_registers[37]
    
    return kwargs

def read_json_file(fp):
    
    kwargs = {}
    
    return kwargs

def write_dds_file(filename):
    pass

def write_json_file(filename):
    pass