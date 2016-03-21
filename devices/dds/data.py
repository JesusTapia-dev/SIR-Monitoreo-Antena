'''
Created on Feb 15, 2016

@author: Miguel Urco
'''
import struct
import string

DDS_NBITS = 48

FILE_STRUCTURE = """Phase Adjust Register 1
-----------------------
00000000
00000000
-----------------------
Phase Adjust Register 2
-----------------------
00000000
00000000
-----------------------
Frequency Tuning Word 1
-----------------------
00000000
00000000
00000000
00000000
00000000
00000000
-----------------------
Frequency Tuning Word 2
-----------------------
00000000
00000000
00000000
00000000
00000000
00000000
-----------------------
Delta Frequency Word
-----------------------
00000000
00000000
00000000
00000000
00000000
00000000
-----------------------
Update Clock
-----------------------
00000000
00000000
00000000
00000000
-----------------------
Ramp Rate Clock
-----------------------
00000000
00000000
00000000
-----------------------
Control Register
-----------------------
00000000
00000000
00000000
00000000
-----------------------
Output Shaped Keying I
Multiplier
-----------------------
00000000
00000000
-----------------------
Output Shaped Keying Q
Multiplier
-----------------------
00000000
00000000
-----------------------
Output Shaped Keying 
Ramp Rate
-----------------------
00000000
-----------------------
QDAC
-----------------------
00000000
00000000
-----------------------
CLOCK INPUT
-----------------------
10.00000000"""
    
def freq_to_binary(freq, mclock):
        
    if not mclock:
        return None
    
    try:
        binary = int((float(freq)/mclock)*(2**DDS_NBITS))
    except:
        return 0
    
    return binary

def binary_to_freq(binary, mclock):
    
    if not mclock:
        return None
    
    try:
        freq = (float(binary)/(2**DDS_NBITS))*mclock
    except:
        return 0
    
    return freq

def phase_to_binary(phase):
    
    try:
        binary = int(float(phase)*8192/180.0)
    except:
        return 0
    
    return binary

def binary_to_phase(binary):
    
    try:
        phase = float(binary)*180.0/8192
    except:
        return 0
    
    return phase

def __fill_dds_dict(parms):
    
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
    
    my_dict.update(parms)
    my_dict['phaseA'] = phase_to_binary(my_dict['phaseA_degrees'])
    my_dict['phaseB'] = phase_to_binary(my_dict['phaseB_degrees'])
    
    pll_range = 0
    if my_dict['clock'] >= 200:
        pll_range = 1
    
    pll_bypass = 0
    if my_dict['multiplier'] < 4:
        pll_bypass = 1
        
    control_register = (1 << 28) + \
                        (pll_range << 22) + (pll_bypass << 21) + \
                        (my_dict['multiplier'] << 16) + \
                        (my_dict['modulation'] << 9) + \
                        (my_dict['amplitude_enabled'] << 5)
    
    my_dict['control_register'] = control_register
    
    return my_dict

def dds_str_to_dict(registers, clock=None):
    
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
    
    frequencyA_Mhz = None
    frequencyB_Mhz = None
    
    if clock:
        mclock = clock*multiplier
        frequencyA_Mhz = binary_to_freq(frequencyA, mclock)
        frequencyB_Mhz = binary_to_freq(frequencyB, mclock)
    
    parms = {'clock' : clock,
            'multiplier' : multiplier,
            'frequencyA' : frequencyA,
            'frequencyB' : frequencyB,
            'frequencyA_Mhz' : frequencyA_Mhz,
            'frequencyB_Mhz' : frequencyB_Mhz,
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
    
    my_dict = __fill_dds_dict(parms)
    
    registers = ""
    
    registers += struct.pack(">H", my_dict['phaseA'])
    registers += struct.pack(">H", my_dict['phaseB'])
    
    registers += struct.pack(">Q", my_dict['frequencyA'])[2:]
    registers += struct.pack(">Q", my_dict['frequencyB'])[2:]
    
    registers += struct.pack(">Q", my_dict['delta_frequency'])[2:]
    
    registers += struct.pack(">I", my_dict['update_clock'])
    
    registers += struct.pack(">I", my_dict['ramp_rate_clock'])[1:]
    
    registers += struct.pack(">I", my_dict['control_register'])
    
    registers += struct.pack(">H", my_dict['amplitudeI'])
    
    registers += struct.pack(">H", my_dict['amplitudeQ'])
    
    registers += chr(my_dict['amplitude_ramp_rate'])
    
    registers += struct.pack(">H", my_dict['qdac'])
    
    return registers

def text_to_dict(lines):
    
    registers = ""
    registers_v2 = []
    
    for this_line in lines:
        this_line = str.strip(this_line)
        
        if str.isalpha(this_line):
            continue
            
        if not str.isdigit(this_line):
            try:
                value = float(this_line)
            except:
                continue
            
            registers_v2.append(value)
            continue
        
        if len(this_line) != 8:
            continue
        
        registers += chr(string.atoi(this_line,2))
    
    mclock = None
    if len(registers_v2) > 0:
        mclock = registers_v2[0]
    
    my_dict = dds_str_to_dict(registers, mclock)
    
    return my_dict

def dict_to_text(parms):
    """
    It creates formatted DDS text using dictionary values.
    """
    my_dict = __fill_dds_dict(parms)
    
    lines = FILE_STRUCTURE.split('\n')
    
    cad = '{0:016b}'.format(my_dict['phaseA'])
    lines[2] = cad[0:8]
    lines[3] = cad[8:16]
    
    cad = '{0:016b}'.format(my_dict['phaseB'])
    lines[7] = cad[0:8]
    lines[8] = cad[8:16]
    
    cad = '{0:048b}'.format(my_dict['frequencyA'])
    lines[12] = cad[0:8]
    lines[13] = cad[8:16]
    lines[14] = cad[16:24]
    lines[15] = cad[24:32]
    lines[16] = cad[32:40]
    lines[17] = cad[40:48]
    
    cad = '{0:048b}'.format(my_dict['frequencyB'])
    lines[21] = cad[0:8]
    lines[22] = cad[8:16]
    lines[23] = cad[16:24]
    lines[24] = cad[24:32]
    lines[25] = cad[32:40]
    lines[26] = cad[40:48]
    
    cad = '{0:048b}'.format(my_dict['delta_frequency'])
    lines[30] = cad[0:8]
    lines[31] = cad[8:16]
    lines[32] = cad[16:24]
    lines[33] = cad[24:32]
    lines[34] = cad[32:40]
    lines[35] = cad[40:48]
    
    cad = '{0:032b}'.format(my_dict['update_clock'])
    lines[39] = cad[0:8]
    lines[40] = cad[8:16]
    lines[41] = cad[16:24]
    lines[42] = cad[24:32]
    
    cad = '{0:024b}'.format(my_dict['ramp_rate_clock'])
    lines[46] = cad[0:8]
    lines[47] = cad[8:16]
    lines[48] = cad[16:24]
    
    cad = '{0:032b}'.format(my_dict['control_register'])
    lines[52] = cad[0:8]
    lines[53] = cad[8:16]
    lines[54] = cad[16:24]
    lines[55] = cad[24:32]
    
    cad = '{0:016b}'.format(my_dict['amplitudeI'])
    lines[60] = cad[0:8]
    lines[61] = cad[8:16]
    
    cad = '{0:016b}'.format(my_dict['amplitudeQ'])
    lines[66] = cad[0:8]
    lines[67] = cad[8:16]
    
    cad = '{0:08b}'.format(my_dict['amplitude_ramp_rate'])
    lines[72] = cad[0:8]
    
    cad = '{0:016b}'.format(my_dict['qdac'])
    lines[76] = cad[0:8]
    lines[77] = cad[8:16]
    
    lines[81] = '%10.8f' %my_dict['clock']
    
    text = '\n'.join(lines)
    
    return text