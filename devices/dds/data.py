'''
Created on Feb 15, 2016

@author: Miguel Urco
'''
import struct

DDS_NBITS = 48

def freq_to_binary(freq, mclock):
        
    binary = (float(freq)/mclock)*(2**DDS_NBITS)
    
    return binary

def binary_to_freq(binary, mclock):
    
    freq = (float(binary)/(2**DDS_NBITS))*mclock
    
    return freq

def phase_to_binary(phase):
    
    binary = float(phase)*8192/180.0
    
    return binary

def binary_to_phase(binary):
    
    phase = float(binary)*180.0/8192
    
    return phase

def dds_str_to_dict(registers):
    
    """
    Output:
        parms   : Dictionary with keys
            multiplier        :
            frequencyA        :
            frequencyB        :
            frequencyA_Mhz        :
            frequencyB_Mhz        :
            modulation        :
            phaseA_degrees    :
            phaseB_degrees    :
            amplitudeI        :
            amplitudeQ        :
    
    """
    
    if not registers:
        return {}
        
    if len(registers) != 0x28:
        return {}
    
    phaseA = struct.unpack('>H', registers[0x0:0x2])[0]
    phaseB = struct.unpack('>H', registers[0x2:0x4])[0]
    
    frequencyA = struct.unpack('>Q', '\x00\x00' + registers[0x04:0x0A])[0]
    frequencyB = struct.unpack('>Q', '\x00\x00' + registers[0x0A:0x10])[0]
    
    delta_frequency = struct.unpack('>Q', '\x00\x00' + registers[0x10:0x16])[0]
    
    update_clock = struct.unpack('>I', registers[0x16:0x1A])[0]
    
    ramp_rate_clock = struct.unpack('>I', '\x00' + registers[0x1A:0x1D])[0]
    
    control_register = struct.unpack('>I', registers[0x1D:0x21])[0]
    
    amplitudeI = struct.unpack('>H', registers[0x21:0x23])[0] 
    amplitudeQ = struct.unpack('>H', registers[0x23:0x25])[0]
    
    amp_ramp_rate = ord(registers[0x25])
    
    qdac = struct.unpack('>H', registers[0x26:0x28])[0]
    
    multiplier          = (control_register & 0x001F0000) >> 16
    modulation          = (control_register & 0x00000E00) >> 9
    amplitude_enabled   = (control_register & 0x00000020) >> 5
    
    parms = {'clock' : None,
            'multiplier' : multiplier,
            'frequencyA' : frequencyA,
            'frequencyB' : frequencyB,
            'frequencyA_Mhz' : None,
            'frequencyB_Mhz' : None,
            'phaseA' : phaseA,
            'phaseB' : phaseB,
            'phaseA_degrees' : binary_to_phase(phaseA),
            'phaseB_degrees' : binary_to_phase(phaseB),
            'modulation' : modulation,
            'amplitudeI' : amplitudeI,
            'amplitudeQ' : amplitudeQ,
            'amplitude_enabled' : amplitude_enabled,
            'delta_frequency' : delta_frequency,
            'update_clock' : update_clock,
            'ramp_rate_clock' : ramp_rate_clock,
            'amp_ramp_rate' : amp_ramp_rate,
            'qdac' : qdac
            }
    
    return parms

def dict_to_dds_str(parms):
    """
    Input:
        parms   : Dictionary with keys
            multiplier        :    4 to 20
            frequencyA        :    0 to (2**48-1) equivalent to: 0 - "Master clock"
            frequencyB        :    0 to (2**48-1) equivalent to: 0 - "Master clock"
            modulation        :    0 to 3
            phaseA_degrees    :    0 - 360 degrees
            phaseB_degrees    :    0 - 360 degrees
            amplitudeI        :    0 to (2**12-1) equivalent to: 0 - 100%
            amplitudeQ        :    0 to (2**12-1) equivalent to: 0 - 100%
    """
    
    my_dict = {'clock' : None,
            'multiplier' : 1,
            'frequencyA' : 0,
            'frequencyB' : 0,
            'frequencyA_Mhz' : 0,
            'frequencyB_Mhz' : 0,
            'phaseA_degress' : 0,
            'phaseB_degress' : 0,
            'modulation' : 0,
            'amplitudeI' : 0,
            'amplitudeQ' : 0,
            'amplitude_enabled' : 0,
            'delta_frequency' : 0,
            'update_clock' : 0,
            'ramp_rate_clock' : 0,
            'amplitude_ramp_rate' : 0,
            'qdac' : 0
            }
    
    print "PArms", parms
    
    my_dict.update(parms)
    my_dict['phaseA'] = phase_to_binary(my_dict['phaseA_degrees'])
    my_dict['phaseB'] = phase_to_binary(my_dict['phaseB_degrees'])
    
    registers = ""
    
    control_register = (my_dict['multiplier'] << 16) + (my_dict['modulation'] << 9) + (my_dict['amplitude_enabled'] << 5)
    
    registers += struct.pack(">H", my_dict['phaseA'])
    registers += struct.pack(">H", my_dict['phaseB'])
    
    registers += struct.pack(">Q", my_dict['frequencyA'])[2:]
    registers += struct.pack(">Q", my_dict['frequencyB'])[2:]
    
    registers += struct.pack(">Q", my_dict['delta_frequency'])[2:]
    
    registers += struct.pack(">I", my_dict['update_clock'])
    
    registers += struct.pack(">I", my_dict['ramp_rate_clock'])[1:]
    
    registers += struct.pack(">I", control_register)
    
    registers += struct.pack(">H", my_dict['amplitudeI'])
    
    registers += struct.pack(">H", my_dict['amplitudeQ'])
    
    registers += chr(my_dict['amplitude_ramp_rate'])
    
    registers += struct.pack(">H", my_dict['qdac'])
    
    return registers