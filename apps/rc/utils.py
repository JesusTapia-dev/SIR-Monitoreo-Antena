import ast
import json
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib import cm

class Pulse_Design_Racp:
    """A class to define the .racp output from Pulse Design """
    def __init__(self):
        self.header        = {'version': '1103', 'data':[]}
        self.radar_param   = {'header': '*****Radar Controller Parameters**********', 'data':[]}
        self.system_param1 = {'header': '******System Parameters*******************', 'data':[]}
        self.system_param2 = {'header': '******System Parameters*******************', 'data':[]}
        self.process_param = {'header': '******Process Parameters******************', 'data':[]}
        self.xml = None

        self.header_fields        = [
            {'name': 'EXPERIMENT TYPE', 'xml': 'Experiment/Process/Signal_pre_processing/Type_of_experiment'},
            {'name': 'EXPERIMENT NAME', 'xml': 'Experiment', 'xml_attr_value':'name'}]
        self.radar_param_fields   = [
            {'name': 'IPP', 'xml': 'Experiment/Controller/IPP/Width'},
            {'name': 'NTX', 'xml': 'Experiment/Controller/NTX'},
            {'name': 'TXA', 'xml': 'Experiment/Controller/Transmitters/TX', 'xml_attr':'id', 'xml_attr_find':'txa', 'xml_sub_pattern':'Width'},
            {'name': 'TXB', 'xml': 'Experiment/Controller/Transmitters/TX', 'xml_attr':'id', 'xml_attr_find':'txb', 'xml_sub_pattern':'Width'},
            {'name': '***', 'xml':'', 'type':'pulse_enable'},
            {'name': '***', 'xml':'', 'type': 'Line4'},
            {'name': '***', 'xml':'', 'type': 'Line5'},
            {'name': '***', 'xml':'', 'type': 'Line6'},
            {'name': '***', 'xml':'', 'type':'txb_delays_info'},
            {'name': '***', 'xml':'', 'type': 'Line7'},
            {'name': 'SAMPLING REFERENCE', 'xml':'Experiment/Controller/Ctl_Setting/Sampling_reference'},
            {'name': 'RELOJ', 'xml':'Experiment/Controller/Clock/Clock_final'},
            {'name': 'CLOCK DIVIDER', 'xml':'Experiment/Controller/Clock/Clock_div', 'hide':['1']},
            {'name': 'TR_BEFORE', 'xml':'Experiment/Controller/Spc_Setting/Time_before'},
            {'name': 'TR_AFTER', 'xml':'Experiment/Controller/Spc_Setting/Time_after'},
            {'name': 'WINDOW IN LINE 5&6', 'xml':'', 'value':'NO'},
            {'name': 'SYNCHRO DELAY', 'xml':'Experiment/Controller/Spc_Setting/Sync_delay', 'hide':['0']}]
        self.system_param1_fields  = [
            {'name': 'Number of Cards', 'xml':'Experiment/Process/JARS/Number_of_cards', 'hide':['0']},
            {'name': '***', 'xml':'', 'type':'cards_info'},
            {'name': '***', 'xml':'', 'type':'channels_info'},
            {'name': 'RAW DATA DIRECTORY', 'xml':'Experiment/Process/Data_storage/Directory'},
            {'name': 'CREATE DIRECTORY PER DAY', 'xml':'Experiment/Process/Data_storage/Directory_per_day', 'type':'checkbox_YES_NO'},
            {'name': 'INCLUDE EXPNAME IN DIRECTORY', 'xml':'Experiment/Process/Data_storage/Expname_in_directory', 'type':'checkbox_YES_NO'}]
        self.system_param2_fields  = [
            {'name': 'ADC Resolution', 'xml':'', 'value':'12'}, # Default is 8, JARS is 12
            {'name': 'PCI DIO BusWidth', 'xml':'', 'value':'32'}, # Default for JARS
            {'name': 'RAW DATA BLOCKS', 'xml':'Experiment/Process/Data_arrangement/Data_blocks'}]
        self.process_param_fields  = [
            {'name': 'DATATYPE', 'xml': 'Experiment/Process/Signal_pre_processing/Type_of_data'},
            {'name': 'DATA ARRANGE', 'xml':'', 'value':'CONTIGUOUS_CH'}, #TODO
            {'name': 'COHERENT INTEGRATION STRIDE', 'xml':'Experiment/Process/Signal_pre_processing/Integration_stride'},
            {'name': '------------------', 'xml':'', 'type':'separator'},
            {'name': 'ACQUIRED PROFILES', 'xml':'Experiment/Process/Data_arrangement/Acquired_profiles'},
            {'name': 'PROFILES PER BLOCK', 'xml':'Experiment/Process/Data_arrangement/Profiles_per_block'},
            {'name': '------------------', 'xml':'', 'type':'separator'},
            {'name': 'BEGIN ON START', 'xml':'Experiment/Process/Schedule/Begin_on_Start', 'type': 'checkbox_YES_NO'},
            {'name': 'BEGIN_TIME', 'xml':'Experiment/Process/Schedule/Start', 'hide':['']},
            {'name': 'END_TIME', 'xml':'Experiment/Process/Schedule/End', 'hide':['']},
            {'name': 'VIEW RAW DATA', 'xml':'Experiment/Process/Data_arrangement/View_raw_data', 'type': 'checkbox_YES_NO'},
            {'name': 'REFRESH RATE', 'xml':'', 'value':'1'}, #TODO
            {'name': '------------------', 'xml':'', 'type':'separator'},
            {'name': 'SEND STATUS TO FTP', 'xml':'', 'type':'checkbox_YES_NO', 'value':'NO'}, #TODO
            {'name': 'FTP SERVER', 'xml':'', 'hide':[None, '']}, #TODO
            {'name': 'FTP USER', 'xml':'', 'hide':[None, '']}, #TODO
            {'name': 'FTP PASSWD', 'xml':'', 'hide':[None, '']}, #TODO
            {'name': 'FTP DIR', 'xml':'', 'hide':[None, '']}, #TODO
            {'name': 'FTP FILE', 'xml':'', 'hide':[None, '']}, #TODO
            {'name': 'FTP INTERVAL', 'xml':'', 'hide':[None, '']}, #TODO
            {'name': 'SAVE STATUS AND BLOCK', 'xml':'', 'type':'checkbox_YES_NO', 'value':'NO'}, #TODO
            {'name': 'GENERATE RTI', 'xml':'', 'type':'checkbox_YES_NO', 'value':'NO'}, #TODO
            {'name': 'SEND RTI AND BLOCK', 'xml':'Process_acquired_profiles', 'type':'checkbox_YES_NO'}, #TODO
            {'name': 'FTP INTERVAL', 'xml':'', 'value':'60'}, #TODO
            {'name': '------------------', 'xml':'', 'type':'separator'},
            {'name': 'COMPORT CONFIG', 'xml':'', 'value':'Com1 CBR_9600 TWOSTOPBITS NOPARITY'}, #TODO
            {'name': 'JAM CONFIGURE FILE', 'xml':'', 'value':''}, #TODO
            {'name': 'ACQUISITION SYSTEM', 'xml':'', 'value':'JARS'}, #TODO
            {'name': '******************', 'xml':'', 'type':'acq_system_config_params'},
            {'name': 'SAVE DATA', 'xml':'', 'value':'YES'}, #TODO
            {'name': '******************', 'xml':'', 'type':'rc_seq_config_params'},
            {'name': 'RC_STOP_SEQUENCE', 'xml':'', 'value':'255,0,255,8'},
            {'name': 'RC_START_SEQUENCE', 'xml':'', 'value':'255,24'}]

    def get_field_value(self, field, user_value):
        if 'type' in field and field['type'] == 'checkbox_YES_NO': # Check for existence of value
            if (user_value is None) or (user_value == 'None'):
                user_value = 'NO'
            elif user_value == 'on':
                user_value = 'YES'
        if 'value' in field and not(user_value): # Replace by default value
            user_value = field['value']
        if 'extra' in field and field['extra'] == 'upper': # Uppercase values
            user_value = user_value.upper()
        return str(user_value)

    def load_xml(self, xml):
        self.xml = xml
        for field in self.header_fields:
            self.add_line_output(self.header['data'], field)
        for field in self.radar_param_fields:
            self.add_line_output(self.radar_param['data'], field)
        for field in self.system_param1_fields:
            self.add_line_output(self.system_param1['data'], field)
        for field in self.system_param2_fields:
            self.add_line_output(self.system_param2['data'], field)
        for field in self.process_param_fields:
            self.add_line_output(self.process_param['data'], field)



    def add_line_output(self, text_array, param_field):
        name = param_field['name']
        xml_l = param_field['xml']
        acq_number_of_cards = int(self.xml.find('Experiment/Process/JARS/Number_of_cards').text)
        acq_channels_per_card = int(self.xml.find('Experiment/Process/JARS/Channels_per_card').text)
        number_of_acq_channels = acq_number_of_cards * acq_channels_per_card

        if 'xml_attr' in param_field and 'xml_attr_find' in param_field:
            sub_pattern = False
            if 'xml_sub_pattern' in param_field:
                sub_pattern = param_field['xml_sub_pattern']
            element = self.xml.find_by_attribute_value(xml_l, param_field['xml_attr'], param_field['xml_attr_find'],sub_pattern)
        else:
            element = self.xml.find(xml_l)

        if 'xml_attr_value' in param_field:
            value = element.get(param_field['xml_attr_value'])
        else:
            value    = ''
            if xml_l == '' and 'value' in param_field:
                value    = param_field['value']
            elif hasattr(element, 'text'):
                value    = element.text

        if 'type' in param_field and param_field['type'] == 'separator': # Check for existence of value
            text_array.append('------------------------------------------')
            return
        if 'type' in param_field and param_field['type'] == 'acq_system_config_params': # Get Acquisition System Parameters and add them
            text_array.append("************JARS CONFIGURATION PARAMETERS************")
            if self.xml.find('Experiment/Process/JARS/Filter').text:
                # Notice that we need to use backslashes for the filter path
                text_array.append("Jars_Filter="+self.xml.find('Experiment/Process/JARS/Filter_dir').text +'\\'+ self.xml.find('Experiment/Process/JARS/Filter').text)
            else:
                text_array.append("Jars_Filter=")
            text_array.append("JARS_Collection_Mode="+self.xml.find('Experiment/Process/JARS/JARS_Collection_Mode').text)
            text_array.append("SAVE_DATA=YES")
            text_array.append("*****************************************************")
            return
        if 'type' in param_field and param_field['type'] == 'rc_seq_config_params': # Get Acquisition System Parameters and add them
            text_array.append("****************RC SEQUENCES******************")
            return
        if 'type' in param_field:
            if param_field['type'] == 'pulse_enable':
                txa_enable = self.xml.find_by_attribute_value('Experiment/Controller/Transmitters/TX', 'id', 'txa', 'Pulses')
                if txa_enable.text is not None:
                    text_array.append('Pulse selection_TXA='+txa_enable.text)
                txb_enable = self.xml.find_by_attribute_value('Experiment/Controller/Transmitters/TX', 'id', 'txb', 'Pulses')
                if txb_enable.text is not None:
                    text_array.append('Pulse selection_TXB='+txb_enable.text)
                tr_enable = self.xml.find('Experiment/Controller/IPP/Pulses')
                if tr_enable.text is not None:
                    text_array.append('Pulse selection_TR='+tr_enable.text)
                return
            elif param_field['type'] == 'Line4' or param_field['type'] == 'Line5' or param_field['type'] == 'Line6' or param_field['type'] == 'Line7':
                code_name = 'Code_A'
                line_number = '4'
                line_parenthesis  = ''
                line_prepend = ''

                if param_field['type'] == 'Line5':
                    code_name = 'Code_B'
                    line_number = '5'
                    line_parenthesis  = ' (Line 5)'
                    line_prepend = 'L5_'
                elif param_field['type'] == 'Line6':
                    code_name = 'Code_C'
                    line_number = '6'
                    line_parenthesis  = ' (Line 6)'
                    line_prepend = 'L6_'
                elif param_field['type'] == 'Line7':
                    code_name = 'Code_D'
                    line_number = '7'
                    line_parenthesis  = ' (Line 7)'
                    line_prepend = 'L7_'

                code_channel = self.xml.find_by_attribute_value('Experiment/Controller/Code_channels/Code_channel', 'id', code_name, 'Mode').text
                if code_channel == 'FLIP':
                    value = self.xml.find_by_attribute_value('Experiment/Controller/Code_channels/Code_channel', 'id', code_name, 'Flip').text
                    flip_name = 'L'+line_number+'_FLIP' + line_parenthesis
                    if param_field['type'] == 'Line5':
                        flip_name = 'FLIP1'
                    elif param_field['type'] == 'Line6':
                        flip_name = 'FLIP2'
                    text_array.append(flip_name + '='+value)
                elif code_channel == 'CODE':
                    code_data = self.xml.find_by_attribute_value('Experiment/Controller/Code_channels/Code_channel', 'id', code_name, 'Code')
                    Code_reference = code_data.find('Code_reference').text
                    Code_select = code_data.find('Code_select').text
                    Code_number = code_data.find('Code_number').text
                    Code_bits = code_data.find('Code_bits').text
                    custom_codes = get_custom_code_data(Code_select, int(Code_number), int(Code_bits))
                    text_array.append('Code Type' + line_parenthesis + '='+Code_select)
                    text_array.append('Number of Codes' + line_parenthesis + '='+Code_number)
                    text_array.append('Code Width' + line_parenthesis + '='+Code_bits)
                    for zero_idx, custom_code in enumerate(custom_codes):
                        text_array.append(line_prepend+'COD('+str(zero_idx)+')='+custom_code)
                    # Calculate Codes
                    text_array.append('L'+line_number+'_REFERENCE='+Code_reference.upper())
                elif code_channel == 'Sampling':
                    sampling_name = 'Sampling Windows (Line ' + line_number + ')'
                    prepend = 'L'+line_number+'_'
                    if param_field['type'] == 'Line7':
                        sampling_name = 'Sampling Windows'
                        prepend = ''
                    sampling_data = self.xml.find_by_attribute_value('Experiment/Controller/Code_channels/Code_channel', 'id', code_name, 'Sampling')
                    Code_reference = sampling_data.find('Code_reference').text.upper()
                    samples = sampling_data.find('Samples')
                    text_array.append(sampling_name+'='+str(len(samples)))
                    for zero_idx, sample in enumerate(samples):
                        text_array.append(prepend+'H0('+str(zero_idx)+')='+sample.find('FH').text)
                        text_array.append(prepend+'NSA('+str(zero_idx)+')='+sample.find('NSA').text)
                        text_array.append(prepend+'DH('+str(zero_idx)+')='+sample.find('DH').text)
                    text_array.append('L'+line_number+'_REFERENCE='+Code_reference.upper())
                elif code_channel == 'Synchro':
                    text_array.append('Line'+line_number+'=Synchro')
                elif code_channel == 'Portion_Spec':
                    portion_data = self.xml.find_by_attribute_value('Experiment/Controller/Code_channels/Code_channel', 'id', code_name, 'PortionSpec')
                    periodic = portion_data.find('Periodic').text
                    portions = portion_data.find('Portions')
                    text_array.append('L'+line_number+' Number Of Portions='+str(len(portions)))
                    for zero_idx, portion in enumerate(portions):
                        text_array.append('PORTION_BEGIN('+str(zero_idx)+')='+portion.find('Begin_units').text)
                        text_array.append('PORTION_END('+str(zero_idx)+')='+portion.find('End_units').text)
                    if periodic == '1':
                        text_array.append('L'+line_number+' Portions IPP Periodic=YES')
                    else:
                        text_array.append('L'+line_number+' Portions IPP Periodic=NO')
                return
            elif param_field['type'] == 'txb_delays_info':
                txb_delays = self.xml.find_by_attribute_value('Experiment/Controller/Transmitters/TX', 'id', 'txb', 'Delays')
                text_array.append("Number of Taus="+str(len(txb_delays)))
                for zero_index, txb_delay in enumerate(txb_delays):
                    text_array.append('TAU('+str(zero_index)+')='+str(txb_delay.text))
                return
            elif param_field['type'] == 'cards_info': # Get Cards info
                if not(acq_number_of_cards == '0'):
                    for card in range(acq_number_of_cards):
                        name = 'Card('+str(card)+')'
                        text_array.append(name + "=" + str(card))
                return
            elif param_field['type'] == 'channels_info': # Get Channel info
                text_array.append("Number of Channels="+str(number_of_acq_channels))
                if not(number_of_acq_channels == '0'):
                    acq_channels = self.xml.find('Experiment/Process/Acq_channel_selection')
                    enabled_channels = []
                    channel_names =[]
                    for acq_channel in acq_channels:
                        acq_channel_number = acq_channel.get('id')
                        acq_channel_name   = acq_channel.find('Name').text
                        enabled = False
                        if hasattr(acq_channel.find('Enabled'), 'text'):
                            enabled =  acq_channel.find('Enabled').text
                        if enabled == 'on':
                            text_array.append("Channel("+acq_channel_number+")=" + str(int(acq_channel_number)+1))
                            enabled_channels.append(acq_channel_number)
                            channel_names.append(acq_channel_name)
                    text_array.append("Antennas_Names="+str(len(enabled_channels)))
                    for index, channel in enumerate(enabled_channels):
                        text_array.append("AntennaName(" + str(int(channel)+1) + ")="+str(channel_names[index]))
                return
        if 'hide' in param_field and value in param_field['hide']: # Check to see if value should be written
            return
        text_array.append(name + "=" + self.get_field_value(param_field, value))

    def convert_to_racp(self):
        output = []
        # HEADER
        for line in self.header['data']:
            output.append(line)
        output.append('HEADER VERSION='+self.header['version'])
        # RADAR PARAMETERS
        output.append(self.radar_param['header'])
        for line in self.radar_param['data']:
            output.append(line)
        # SYSTEM PARAMETERS
        output.append(self.system_param1['header'])
        for line in self.system_param1['data']:
            output.append(line)
        output.append(self.system_param2['header'])
        for line in self.system_param2['data']:
            output.append(line)
        # PROCESS PARAMETERS
        output.append(self.process_param['header'])
        for line in self.process_param['data']:
            output.append(line)

        racp_content = "\n".join([str(x) for x in output])
        return racp_content

def reduce_code_bits(code_bits, bits_per_code):
    return code_bits[:bits_per_code]

def zeropad_code_bits(code_bits, custom_bits_per_code):
    return code_bits.ljust(custom_bits_per_code, "0")


def get_custom_code_data(codename, number_of_codes, bits_per_code):
    import json
    import copy
    json_data=open('../js/pulse_code_values.json')
    PD_pulse_codes = json.load(json_data)
    selected_code = copy.copy(PD_pulse_codes[codename])

    modified_binary_codes = []
    for i in range (number_of_codes):
        if (i >= selected_code['number_of_codes']):
            # We just repeat the first code.
            modified_binary_codes.append(selected_code['binary_codes'][0])
        else:
            modified_binary_codes.append(selected_code['binary_codes'][i])
    # Now adjust the width
    if (bits_per_code <= selected_code['bits_per_code']):
        modified_binary_codes = [reduce_code_bits(x, bits_per_code) for x in modified_binary_codes]
    else: # Zero pad to the right
        modified_binary_codes = [zeropad_code_bits(x, bits_per_code) for x in modified_binary_codes]
    return modified_binary_codes

class Pulse_Design_Mixed_Racp:
    """A class to define the .racp output from Pulse Design """
    def __init__(self, number_of_experiments):
        self.header        = {'version': '1103'}
        self.radar_param   = {'header': '*****Radar Controller Parameters**********'}
        self.system_param1 = {'header': '******System Parameters*******************'}
        self.system_param2 = {'header': '******System Parameters*******************'}
        self.process_param = {'header': '******Process Parameters******************'}
        self.xml = None
        self.number_of_experiments = number_of_experiments
        self.header_fields = {}
        self.radar_param_fields = {}
        self.system_param1_fields = {}
        self.system_param2_fields = {}
        self.process_param_fields = {}

        for i in range(self.number_of_experiments):
            self.header['data_experiment_number_'+str(i)] = []
            self.radar_param['data_experiment_number_'+str(i)] = []
            self.system_param1['data_experiment_number_'+str(i)] = []
            self.system_param2['data_experiment_number_'+str(i)] = []
            self.process_param['data_experiment_number_'+str(i)] = []

            self.header_fields['indices_experiment_number_'+str(i)] = []
            self.radar_param_fields['indices_experiment_number_'+str(i)] = []
            self.system_param1_fields['indices_experiment_number_'+str(i)] = []
            self.system_param2_fields['indices_experiment_number_'+str(i)] = []
            self.process_param_fields['indices_experiment_number_'+str(i)] = []

            self.header_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'EXPERIMENT TYPE', 'xml': 'Experiments/List/Experiment['+str(i)+']/XML_contents/Pulse_Design/Experiment/Process/Signal_pre_processing/Type_of_experiment'})
            self.header_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'EXPERIMENT NAME', 'xml': 'Experiments/List/Experiment['+str(i)+']/XML_contents/Pulse_Design/Experiment', 'xml_attr_value':'name'})
            self.radar_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'IPP', 'xml': 'Experiments/List/Experiment['+str(i)+']/XML_contents/Pulse_Design/Experiment/Controller/IPP/Width'})
            self.radar_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'NTX', 'xml': 'Experiments/List/Experiment['+str(i)+']/XML_contents/Pulse_Design/Experiment/Controller/NTX'})
            self.radar_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'TXA', 'xml': 'Experiments/List/Experiment['+str(i)+']/XML_contents/Pulse_Design/Experiment/Controller/Transmitters/TX', 'xml_attr':'id', 'xml_attr_find':'txa', 'xml_sub_pattern':'Width'})
            self.radar_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'TXB', 'xml': 'Experiments/List/Experiment['+str(i)+']/XML_contents/Pulse_Design/Experiment/Controller/Transmitters/TX', 'xml_attr':'id', 'xml_attr_find':'txb', 'xml_sub_pattern':'Width'})
            self.radar_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': '***', 'xml':'', 'type':'pulse_enable'})
            self.radar_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': '***', 'xml':'', 'type': 'Line4'})
            self.radar_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': '***', 'xml':'', 'type': 'Line5'})
            self.radar_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': '***', 'xml':'', 'type': 'Line6'})
            self.radar_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': '***', 'xml':'', 'type':'txb_delays_info'})
            self.radar_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': '***', 'xml':'', 'type': 'Line7'})
            self.radar_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'SAMPLING REFERENCE', 'xml':'Experiments/List/Experiment['+str(i)+']/XML_contents/Pulse_Design/Experiment/Controller/Ctl_Setting/Sampling_reference'})
            self.radar_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'RELOJ', 'xml':'Experiments/List/Experiment['+str(i)+']/XML_contents/Pulse_Design/Experiment/Controller/Clock/Clock_final'})
            self.radar_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'CLOCK DIVIDER', 'xml':'Experiments/List/Experiment['+str(i)+']/XML_contents/Pulse_Design/Experiment/Controller/Clock/Clock_div', 'hide':['1']})
            self.radar_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'TR_BEFORE', 'xml':'Experiments/List/Experiment['+str(i)+']/XML_contents/Pulse_Design/Experiment/Controller/Spc_Setting/Time_before'})
            self.radar_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'TR_AFTER', 'xml':'Experiments/List/Experiment['+str(i)+']/XML_contents/Pulse_Design/Experiment/Controller/Spc_Setting/Time_after'})
            self.radar_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'WINDOW IN LINE 5&6', 'xml':'', 'value':'NO'})
            self.radar_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'SYNCHRO DELAY', 'xml':'Experiments/List/Experiment['+str(i)+']/XML_contents/Pulse_Design/Experiment/Controller/Spc_Setting/Sync_delay', 'hide':['0']})
            self.system_param1_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'Number of Cards', 'xml':'Experiments/List/Experiment['+str(i)+']/XML_contents/Pulse_Design/Experiment/Process/JARS/Number_of_cards', 'hide':['0']})
            self.system_param1_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': '***', 'xml':'', 'type':'cards_info'})
            self.system_param1_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': '***', 'xml':'', 'type':'channels_info'})
            self.system_param1_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'RAW DATA DIRECTORY', 'xml':'Experiments/List/Experiment['+str(i)+']/XML_contents/Pulse_Design/Experiment/Process/Data_storage/Directory'})
            self.system_param1_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'CREATE DIRECTORY PER DAY', 'xml':'Experiments/List/Experiment['+str(i)+']/XML_contents/Pulse_Design/Experiment/Process/Data_storage/Directory_per_day', 'type':'checkbox_YES_NO'})
            self.system_param1_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'INCLUDE EXPNAME IN DIRECTORY', 'xml':'Experiments/List/Experiment['+str(i)+']/XML_contents/Pulse_Design/Experiment/Process/Data_storage/Expname_in_directory', 'type':'checkbox_YES_NO'})
            self.system_param2_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'ADC Resolution', 'xml':'', 'value':'12'})# Default is 8, JARS is 12
            self.system_param2_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'PCI DIO BusWidth', 'xml':'', 'value':'32'}) # Default for JARS
            self.system_param2_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'RAW DATA BLOCKS', 'xml':'Experiments/List/Experiment['+str(i)+']/XML_contents/Pulse_Design/Experiment/Process/Data_arrangement/Data_blocks'})
            self.process_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'DATATYPE', 'xml': 'Experiments/List/Experiment['+str(i)+']/XML_contents/Pulse_Design/Experiment/Process/Signal_pre_processing/Type_of_data'})
            self.process_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'DATA ARRANGE', 'xml':'', 'value':'CONTIGUOUS_CH'})
            self.process_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'COHERENT INTEGRATION STRIDE', 'xml':'Experiments/List/Experiment['+str(i)+']/XML_contents/Pulse_Design/Experiment/Process/Signal_pre_processing/Integration_stride'})
            self.process_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': '------------------', 'xml':'', 'type':'separator'})
            self.process_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'ACQUIRED PROFILES', 'xml':'Experiments/List/Experiment['+str(i)+']/XML_contents/Pulse_Design/Experiment/Process/Data_arrangement/Acquired_profiles'})
            self.process_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'PROFILES PER BLOCK', 'xml':'Experiments/List/Experiment['+str(i)+']/XML_contents/Pulse_Design/Experiment/Process/Data_arrangement/Profiles_per_block'})
            self.process_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': '------------------', 'xml':'', 'type':'separator'})
            self.process_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'BEGIN ON START', 'xml':'Experiments/List/Experiment['+str(i)+']/XML_contents/Pulse_Design/Experiment/Process/Schedule/Begin_on_Start', 'type': 'checkbox_YES_NO'})
            self.process_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'BEGIN_TIME', 'xml':'Experiments/List/Experiment['+str(i)+']/XML_contents/Pulse_Design/Experiment/Process/Schedule/Start', 'hide':['']})
            self.process_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'END_TIME', 'xml':'Experiments/List/Experiment['+str(i)+']/XML_contents/Pulse_Design/Experiment/Process/Schedule/End', 'hide':['']})
            self.process_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'VIEW RAW DATA', 'xml':'Experiments/List/Experiment['+str(i)+']/XML_contents/Pulse_Design/Experiment/Process/Data_arrangement/View_raw_data', 'type': 'checkbox_YES_NO'})
            self.process_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'REFRESH RATE', 'xml':'', 'value':'1'})
            self.process_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': '------------------', 'xml':'', 'type':'separator'})
            self.process_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'SEND STATUS TO FTP', 'xml':'', 'type':'checkbox_YES_NO', 'value':'NO'})
            self.process_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'FTP SERVER', 'xml':'', 'hide':[None, '']})
            self.process_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'FTP USER', 'xml':'', 'hide':[None, '']})
            self.process_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'FTP PASSWD', 'xml':'', 'hide':[None, '']})
            self.process_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'FTP DIR', 'xml':'', 'hide':[None, '']})
            self.process_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'FTP FILE', 'xml':'', 'hide':[None, '']})
            self.process_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'FTP INTERVAL', 'xml':'', 'hide':[None, '']})
            self.process_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'SAVE STATUS AND BLOCK', 'xml':'', 'type':'checkbox_YES_NO', 'value':'NO'})
            self.process_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'GENERATE RTI', 'xml':'', 'type':'checkbox_YES_NO', 'value':'NO'})
            self.process_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'SEND RTI AND BLOCK', 'xml':'Process_acquired_profiles', 'type':'checkbox_YES_NO'})
            self.process_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'FTP INTERVAL', 'xml':'', 'value':'60'})
            self.process_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': '------------------', 'xml':'', 'type':'separator'})
            self.process_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'COMPORT CONFIG', 'xml':'', 'value':'Com1 CBR_9600 TWOSTOPBITS NOPARITY'})
            self.process_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'JAM CONFIGURE FILE', 'xml':'', 'value':''})
            self.process_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'ACQUISITION SYSTEM', 'xml':'', 'value':'JARS'})
            self.process_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': '******************', 'xml':'', 'type':'acq_system_config_params'})
            self.process_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'SAVE DATA', 'xml':'', 'value':'YES'})
            self.process_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': '******************', 'xml':'', 'type':'rc_seq_config_params'})
            self.process_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'RC_STOP_SEQUENCE', 'xml':'', 'value':'255,0,255,8'})
            self.process_param_fields['indices_experiment_number_'+str(i)].append({'number_experiment': i,'name': 'RC_START_SEQUENCE', 'xml':'', 'value':'255,24'})
    def get_field_value(self, field, user_value):
        if 'type' in field and field['type'] == 'checkbox_YES_NO': # Check for existence of value
            if (user_value is None) or (user_value == 'None'):
                user_value = 'NO'
            elif user_value == 'on':
                user_value = 'YES'
        if 'value' in field and not(user_value): # Replace by default value
            user_value = field['value']
        if 'extra' in field and field['extra'] == 'upper': # Uppercase values
            user_value = user_value.upper()
        return str(user_value)

    def load_xml(self, xml):
        self.xml = xml
        for i in range(self.number_of_experiments):
            for field in self.header_fields['indices_experiment_number_'+str(i)]:
                self.add_line_output(self.header['data_experiment_number_'+str(i)], field)
            for field in self.radar_param_fields['indices_experiment_number_'+str(i)]:
                self.add_line_output(self.radar_param['data_experiment_number_'+str(i)], field)
            for field in self.system_param1_fields['indices_experiment_number_'+str(i)]:
                self.add_line_output(self.system_param1['data_experiment_number_'+str(i)], field)
            for field in self.system_param2_fields['indices_experiment_number_'+str(i)]:
                self.add_line_output(self.system_param2['data_experiment_number_'+str(i)], field)
            for field in self.process_param_fields['indices_experiment_number_'+str(i)]:
                self.add_line_output(self.process_param['data_experiment_number_'+str(i)], field)



    def add_line_output(self, text_array, param_field):


        name     = param_field['name']
        xml_l    = param_field['xml']
        id = str(param_field['number_experiment'])
        acq_number_of_cards    = int(self.xml.find('Experiments/List/Experiment['+id+']/XML_contents/Pulse_Design/Experiment/Process/JARS/Number_of_cards').text)
        acq_channels_per_card  = int(self.xml.find('Experiments/List/Experiment['+id+']/XML_contents/Pulse_Design/Experiment/Process/JARS/Channels_per_card').text)
        number_of_acq_channels = acq_number_of_cards * acq_channels_per_card



        if 'xml_attr' in param_field and 'xml_attr_find' in param_field:
            sub_pattern = False
            if 'xml_sub_pattern' in param_field:
                sub_pattern = param_field['xml_sub_pattern']
            element = self.xml.find_by_attribute_value(xml_l, param_field['xml_attr'], param_field['xml_attr_find'],sub_pattern)
        else:
            element = self.xml.find(xml_l)

        if 'xml_attr_value' in param_field:
            value    = element.get(param_field['xml_attr_value'])
        else:
            value    = ''
            if xml_l == '' and 'value' in param_field:
                value    = param_field['value']
            elif hasattr(element, 'text'):
                value    = element.text

        if 'type' in param_field and param_field['type'] == 'separator': # Check for existence of value
            text_array.append('------------------------------------------')
            return
        if 'type' in param_field and param_field['type'] == 'acq_system_config_params': # Get Acquisition System Parameters and add them
            text_array.append("************JARS CONFIGURATION PARAMETERS************")
            if self.xml.find('Experiments/List/Experiment['+id+']/XML_contents/Pulse_Design/Experiment/Process/JARS/Filter').text:
                # Notice that we need to use backslashes for the filter path
                text_array.append("Jars_Filter="+self.xml.find('Experiments/List/Experiment['+id+']/XML_contents/Pulse_Design/Experiment/Process/JARS/Filter_dir').text +'\\'+ self.xml.find('Experiments/List/Experiment['+id+']/XML_contents/Pulse_Design/Experiment/Process/JARS/Filter').text)
            else:
                text_array.append("Jars_Filter=")
            text_array.append("JARS_Collection_Mode="+self.xml.find('Experiments/List/Experiment['+id+']/XML_contents/Pulse_Design/Experiment/Process/JARS/JARS_Collection_Mode').text)
            text_array.append("SAVE_DATA=YES")
            text_array.append("*****************************************************")
            return
        if 'type' in param_field and param_field['type'] == 'rc_seq_config_params': # Get Acquisition System Parameters and add them
            text_array.append("****************RC SEQUENCES******************")
            return
        ##{'name': '***', 'xml':'', 'type':'pulse_enable'},
        if 'type' in param_field:
            if param_field['type'] == 'pulse_enable':
                txa_enable = self.xml.find_by_attribute_value('Experiments/List/Experiment['+id+']/XML_contents/Pulse_Design/Experiment/Controller/Transmitters/TX', 'id', 'txa', 'Pulses')
                if txa_enable.text is not None:
                    text_array.append('Pulse selection_TXA='+txa_enable.text)
                txb_enable = self.xml.find_by_attribute_value('Experiments/List/Experiment['+id+']/XML_contents/Pulse_Design/Experiment/Controller/Transmitters/TX', 'id', 'txb', 'Pulses')
                if txb_enable.text is not None:
                    text_array.append('Pulse selection_TXB='+txb_enable.text)
                tr_enable = self.xml.find('Experiments/List/Experiment['+id+']/XML_contents/Pulse_Design/Experiment/Controller/IPP/Pulses')
                if tr_enable.text is not None:
                    text_array.append('Experiments/List/Experiment['+id+']/XML_contents/Pulse_Design/Pulse selection_TR='+tr_enable.text)
                return
            elif param_field['type'] == 'Line4' or param_field['type'] == 'Line5' or param_field['type'] == 'Line6' or param_field['type'] == 'Line7':
                code_name = 'Code_A'
                line_number = '4'
                line_parenthesis  = ''
                line_prepend = ''

                if param_field['type'] == 'Line5':
                    code_name = 'Code_B'
                    line_number = '5'
                    line_parenthesis  = ' (Line 5)'
                    line_prepend = 'L5_'
                elif param_field['type'] == 'Line6':
                    code_name = 'Code_C'
                    line_number = '6'
                    line_parenthesis  = ' (Line 6)'
                    line_prepend = 'L6_'
                elif param_field['type'] == 'Line7':
                    code_name = 'Code_D'
                    line_number = '7'
                    line_parenthesis  = ' (Line 7)'
                    line_prepend = 'L7_'

                code_channel = self.xml.find_by_attribute_value('Experiments/List/Experiment['+id+']/XML_contents/Pulse_Design/Experiment/Controller/Code_channels/Code_channel', 'id', code_name, 'Mode').text
                if code_channel == 'FLIP':
                    value = self.xml.find_by_attribute_value('Experiments/List/Experiment['+id+']/XML_contents/Pulse_Design/Experiment/Controller/Code_channels/Code_channel', 'id', code_name, 'Flip').text
                    flip_name = 'L'+line_number+'_FLIP' + line_parenthesis
                    if param_field['type'] == 'Line5':
                        flip_name = 'FLIP1'
                    elif param_field['type'] == 'Line6':
                        flip_name = 'FLIP2'
                    text_array.append(flip_name + '='+value)
                elif code_channel == 'CODE':
                    code_data = self.xml.find_by_attribute_value('Experiments/List/Experiment['+id+']/XML_contents/Pulse_Design/Experiment/Controller/Code_channels/Code_channel', 'id', code_name, 'Code')
                    Code_reference = code_data.find('Code_reference').text
                    Code_select = code_data.find('Code_select').text
                    Code_number = code_data.find('Code_number').text
                    Code_bits = code_data.find('Code_bits').text
                    custom_codes = get_custom_code_data(Code_select, int(Code_number), int(Code_bits))
                    text_array.append('Code Type' + line_parenthesis + '='+Code_select)
                    text_array.append('Number of Codes' + line_parenthesis + '='+Code_number)
                    text_array.append('Code Width' + line_parenthesis + '='+Code_bits)
                    for zero_idx, custom_code in enumerate(custom_codes):
                        text_array.append(line_prepend+'COD('+str(zero_idx)+')='+custom_code)
                    # Calculate Codes
                    text_array.append('L'+line_number+'_REFERENCE='+Code_reference.upper())
                elif code_channel == 'Sampling':
                    sampling_name = 'Sampling Windows (Line ' + line_number + ')'
                    prepend = 'L'+line_number+'_'
                    if param_field['type'] == 'Line7':
                        sampling_name = 'Sampling Windows'
                        prepend = ''
                    sampling_data = self.xml.find_by_attribute_value('Experiments/List/Experiment['+id+']/XML_contents/Pulse_Design/Experiment/Controller/Code_channels/Code_channel', 'id', code_name, 'Sampling')
                    Code_reference = sampling_data.find('Code_reference').text.upper()
                    samples = sampling_data.find('Samples')
                    text_array.append(sampling_name+'='+str(len(samples)))
                    for zero_idx, sample in enumerate(samples):
                        text_array.append(prepend+'H0('+str(zero_idx)+')='+sample.find('FH').text)
                        text_array.append(prepend+'NSA('+str(zero_idx)+')='+sample.find('NSA').text)
                        text_array.append(prepend+'DH('+str(zero_idx)+')='+sample.find('DH').text)
                    text_array.append('L'+line_number+'_REFERENCE='+Code_reference.upper())
                elif code_channel == 'Synchro':
                    text_array.append('Line'+line_number+'=Synchro')
                elif code_channel == 'Portion_Spec':
                    portion_data = self.xml.find_by_attribute_value('Experiments/List/Experiment['+id+']/XML_contents/Pulse_Design/Experiment/Controller/Code_channels/Code_channel', 'id', code_name, 'PortionSpec')
                    periodic = portion_data.find('Periodic').text
                    portions = portion_data.find('Portions')
                    text_array.append('L'+line_number+' Number Of Portions='+str(len(portions)))
                    for zero_idx, portion in enumerate(portions):
                        text_array.append('PORTION_BEGIN('+str(zero_idx)+')='+portion.find('Begin_units').text)
                        text_array.append('PORTION_END('+str(zero_idx)+')='+portion.find('End_units').text)
                    if periodic == '1':
                        text_array.append('L'+line_number+' Portions IPP Periodic=YES')
                    else:
                        text_array.append('L'+line_number+' Portions IPP Periodic=NO')
                return
            elif param_field['type'] == 'txb_delays_info':
                txb_delays = self.xml.find_by_attribute_value('Experiments/List/Experiment['+id+']/XML_contents/Pulse_Design/Experiment/Controller/Transmitters/TX', 'id', 'txb', 'Delays')
                text_array.append("Number of Taus="+str(len(txb_delays)))
                for zero_index, txb_delay in enumerate(txb_delays):
                    text_array.append('TAU('+str(zero_index)+')='+str(txb_delay.text))
                return
            elif param_field['type'] == 'cards_info': # Get Cards info
                if not(acq_number_of_cards == '0'):
                    for card in range(acq_number_of_cards):
                        name = 'Card('+str(card)+')'
                        text_array.append(name + "=" + str(card))
                return
            elif param_field['type'] == 'channels_info': # Get Channel info
                text_array.append("Number of Channels="+str(number_of_acq_channels))
                if not(number_of_acq_channels == '0'):
                    acq_channels = self.xml.find('Experiments/List/Experiment['+id+']/XML_contents/Pulse_Design/Experiment/Process/Acq_channel_selection')
                    enabled_channels = []
                    channel_names =[]
                    for acq_channel in acq_channels:
                        acq_channel_number = acq_channel.get('id')
                        acq_channel_name   = acq_channel.find('Name').text
                        enabled = False
                        if hasattr(acq_channel.find('Enabled'), 'text'):
                            enabled =  acq_channel.find('Enabled').text
                        if enabled == 'on':
                            text_array.append("Channel("+acq_channel_number+")=" + str(int(acq_channel_number)+1))
                            enabled_channels.append(acq_channel_number)
                            channel_names.append(acq_channel_name)
                    text_array.append("Antennas_Names="+str(len(enabled_channels)))
                    for index, channel in enumerate(enabled_channels):
                        text_array.append("AntennaName(" + str(int(channel)+1) + ")="+str(channel_names[index]))
                return
        if 'hide' in param_field and value in param_field['hide']: # Check to see if value should be written
            return
        text_array.append(name + "=" + self.get_field_value(param_field, value))

    def convert_to_racp(self):
        output = []
        # HEADER
        for i in range(self.number_of_experiments):
            for line in self.header['data_experiment_number_'+str(i)]:
                output.append(line)
            output.append('HEADER VERSION='+self.header['version'])
            # RADAR PARAMETERS
            output.append(self.radar_param['header'])
            for line in self.radar_param['data_experiment_number_'+str(i)]:
                output.append(line)
            # SYSTEM PARAMETERS
            output.append(self.system_param1['header'])
            for line in self.system_param1['data_experiment_number_'+str(i)]:
                output.append(line)
            output.append(self.system_param2['header'])
            for line in self.system_param2['data_experiment_number_'+str(i)]:
                output.append(line)
            # PROCESS PARAMETERS
            output.append(self.process_param['header'])
            for line in self.process_param['data_experiment_number_'+str(i)]:
                output.append(line)
            output.append("\n")

        racp_content = "\n".join([str(x) for x in output])
        return racp_content

class RCFile(object):
    
    def __init__(self, f=None):
        
        self.data = {}
        if isinstance(f, str):
            self.f = open(f)
            self.name = f.split('/')[-1]
        elif hasattr(f, 'read'):
            self.f = f
            self.name = f.name.split('/')[-1]
        else:
            self.f = f
            self.name = None
            
        if self.f:
            if 'racp' in self.name:
                self.parse_racp()
            elif 'dat' in self.name:
                self.parse_dat()

    def get_line_parameters(self, data, line):
        
        line_params = {}
        for label in data:
            if 'L%d' % line in label or '(Line %d)' % line in label or 'Line%d' % line in label:
                line_params[label] = data[label]
        return line_params

    def parse_racp(self):
        
        data = {}
        raw_data =  [s.strip() for s in self.f.readlines()]
        for line in raw_data:
            if line and '=' in line:
                label, value = line.strip().split('=')
                data[label] = value
        self.data['experiment_type'] = data['EXPERIMENT TYPE']
        self.data['header_version'] = data['HEADER VERSION']
        self.data['name'] = data['EXPERIMENT NAME']
        self.data['ipp'] = float(data['IPP'])
        self.data['ntx'] = int(data['NTX'])
        if 'CLOCK DIVIDER' in data:
            self.data['clock_divider'] = int(data['CLOCK DIVIDER'])
        else:
            self.data['clock_divider'] = 1
        self.data['clock'] = float(data['RELOJ'])*self.data['clock_divider']
        self.data['time_before'] = int(data['TR_BEFORE'])
        self.data['time_after'] = int(data['TR_AFTER'])
        if 'SYNCHRO DELAY' in data:
            self.data['sync'] = int(data['SYNCHRO DELAY'])
        else:
            self.data['sync'] = 0
        self.data['lines'] = []
        
        #Add TR line
        if 'Pulse selection_TR' in data:
            if 'A' in data['Pulse selection_TR']:
                rng = data['Pulse selection_TR'].replace('A', '')
            elif 'B' in data['Pulse selection_TR']:
                rng = data['Pulse selection_TR'].replace('B', '')
            else:
                rng = data['Pulse selection_TR']
            line = {'type':'tr', 'range': rng, 'TX_ref':'TXA'}
        else:
            line = {'type': 'tr', 'range': 0, 'TX_ref': '0'}
        
        self.data['lines'].append(line)
        
        #Add TX's lines
        if 'TXA' in data:
            line = {'type':'tx', 'pulse_width':data['TXA'], 'delays':'0'}
            if 'Pulse selection_TXA' in data:
                line['range'] = data['Pulse selection_TXA']
            else:
                line['range'] = '0'
            self.data['lines'].append(line)
        
        if 'TXB' in data:
            line = {'type':'tx', 'pulse_width':data['TXB'], 'delays':'0'}
            if 'Pulse selection_TXB' in data:
                line['range'] = data['Pulse selection_TXB']
            else:
                line['range'] = '0'
            
            if 'Number of Taus' in data:
                delays = [data['TAU({0})'.format(i)] for i in range(int(data['Number of Taus']))]
                line['delays'] = ','.join(delays)
                
            self.data['lines'].append(line)
        
        #Add Other lines (4-6)
        for n in range(4, 7):
            params = self.get_line_parameters(data, n)
            labels = params.keys()
            
            if 'L%d_FLIP' % n in labels:
                line = {'type':'flip', 'number_of_flips':data['L%d_FLIP' % n]}
            elif 'Code Type' in data and n==4:
                line = {'type':'codes', 'code':data['Code Type'], 'TX_ref':data['L%d_REFERENCE' % n]}
            elif 'Code Type (Line %d)' % n in labels:
                line = {'type':'codes', 'code':data['Code Type (Line %d)' % n], 'TX_ref':data['L%d_REFERENCE' % n]}
            elif 'Sampling Windows (Line %d)' % n in data:
                line = {'type':'windows', 'TX_ref':data['L%d_REFERENCE' % n]}
                windows = []
                for w in range(int(data['Sampling Windows (Line %d)' % n])):
                    windows.append({'first_height':float(data['L%d_H0(%d)' % (n, w)]),
                         'number_of_samples':int(data['L%d_NSA(%d)' % (n, w)]),
                         'resolution':float(data['L%d_DH(%d)' % (n, w)])}
                        )
                line['params'] = windows
            elif 'Line%d' % n in labels and data['Line%d' % n]=='Synchro':
                line = {'type':'sync', 'invert':0}
            elif 'L%d Number Of Portions' % n in labels:
                line = {'type':'prog_pulses'}
                if 'L%s Portions IPP Periodic' % n in data:
                    line['periodic'] = 1 if data['L%s Portions IPP Periodic' % n]=='YES' else 0
                portions = []
                x = raw_data.index('L%d Number Of Portions=%s' % (n, data['L%d Number Of Portions' % n]))
                for w in range(int(data['L%d Number Of Portions' % n])):
                    begin = raw_data[x+1+2*w].split('=')[-1]
                    end = raw_data[x+2+2*w].split('=')[-1]
                    portions.append({'begin':int(begin),
                         'end':int(end)}
                        )
                line['params'] = portions
            elif 'FLIP1' in data and n==5:
                line = {'type':'flip', 'number_of_flips':data['FLIP1']}
            elif 'FLIP2' in data and n==6:
                line = {'type':'flip', 'number_of_flips':data['FLIP2']}    
            else:
                line = {'type':'none'}    
                
            self.data['lines'].append(line)
            
        #Add line 7 (windows)
        if 'Sampling Windows' in data:
            line = {'type':'windows', 'TX_ref':data['L7_REFERENCE']}
            windows = []
            x = raw_data.index('Sampling Windows=%s' % data['Sampling Windows'])
            for w in range(int(data['Sampling Windows'])):
                h0 = raw_data[x+1+3*w].split('=')[-1]
                nsa = raw_data[x+2+3*w].split('=')[-1]
                dh = raw_data[x+3+3*w].split('=')[-1]
                windows.append({'first_height':float(h0),
                     'number_of_samples':int(nsa),
                     'resolution':float(dh)}
                    )
            line['params'] = windows
            self.data['lines'].append(line)
        else:
            self.data['lines'].append({'type':'none'})
    
        #Add line 8 (synchro inverted)
        self.data['lines'].append({'type':'sync', 'invert':1})
    
        return
    
    def parse_dat(self):
        pass
        

    def get_json(self, indent=None):
        return json.dumps(self.data, indent=indent)


def pulses_to_bar(X):


    d = X[1:]-X[:-1]
    
    up = np.where(d==1)[0]
    if X[0]==1:
        up = np.concatenate((np.array([-1]), up))
    up += 1
    
    dw = np.where(d==-1)[0]
    if X[-1]==1:
        dw = np.concatenate((dw, np.array([len(X)-1])))
    dw += 1

    return [(tup[0], tup[1]-tup[0]) for tup in zip(up, dw)]
        

def pulses_from_code(ipp, ntx, codes, width, before=0):
    
    if ntx>len(codes):
        ipp_codes = [c for __ in xrange(ntx) for c in codes][:ntx]
    else:
        ipp_codes = codes[:ntx]
    
    f = width/len(codes[0])
    
    ipp_codes = [''.join([s*f for s in code]) for code in ipp_codes]
    
    if before>0:
        sbefore = '{0:0{1}d}'.format(0, before)
    else:
        sbefore = ''
    
    temp = ['{0}{1}{2:0{3}d}'.format(sbefore, ipp_codes[i], 0, int(ipp)-len(ipp_codes[i])-before) for i in range(ntx)]
    
    return (np.fromstring(''.join(temp), dtype=np.uint8)-48).astype(np.int8)
    

def create_mask(ranges, ipp, ntx, sync):
    
    x = np.arange(ipp*ntx)
    iranges = set()
    
    for index in ranges:
        if '-' in index:
            args = [int(a) for a in index.split('-')]
            iranges = iranges.union([i for i in range(args[0], args[1]+1)])
        else:
            iranges.add(int(index)) 

    y = np.any([(x>=(idx-1)*ipp+sync) & (x<idx*ipp+sync) for idx in iranges], axis=0).astype(np.int8)
    
    return y


def pulses(X, period, width, delay=0, before=0, after=0, sync=0, shift=0):
    
    delay_array = delay
    
    if isinstance(delay, (list, tuple)):
        delay_array = np.ones(len(X))
        delays = [d for __ in xrange(len(X)/(period*len(delay))) for d in delay]
        for i, delay in enumerate(delays):
            delay_array[np.arange(period*i, period*(i+1))] *= delay
    
    if after>0:
        width += after+before
        before = 0
    
    Y = ((X%period<width+delay_array+before+sync) & (X%period>=delay_array+before+sync)).astype(np.int8)
    
    if shift>0:
        y = np.empty_like(Y)
        y[:shift] = 0
        y[shift:] = Y[:-shift]        
        return y
    else:
        return Y  


def plot_pulses(unit, maximun, lines):

    from bokeh.resources import CDN
    from bokeh.embed import components
    from bokeh.mpl import to_bokeh
    from bokeh.plotting import figure
    from bokeh.models.tools import WheelZoomTool, ResetTool, PanTool, PreviewSaveTool
    
    
    N = len(lines)
    fig = plt.figure(figsize=(10, 2+N*0.5))
    ax = fig.add_subplot(111)
    labels = []
    data = []
    for i, line in enumerate(lines):
        print line
        labels.append(line.get_name())
        ax.broken_barh(pulses_to_bar(line.pulses_as_array()), (N-i-1, 0.5), 
                       edgecolor='none', facecolor='#2c3e50')
        #data.append(line.pulses_as_array())

    
    #labels.append('{:3.2f} Km'.format(unit*100))
    #ax.broken_barh(pulses_to_bar(pulses(np.arange(0, maximun), 200, 100)), (0, 0.5), 
    #               edgecolor='none', facecolor='#ae3910')
    
    
    #ax.pcolor(data, cmap=cm.Blues, vmin=0, vmax=1)
    
    labels.reverse()
    #plot = figure(x_range=[0, maximun], y_range=[0, N])
    #plot.image(image=[np.logical_not(data).astype(np.int8)], x=[0], y=[0], dh=[N], dw=[maximun], palette='Blues9')
    ax.set_yticklabels(labels)
    plot = to_bokeh(fig, use_pandas=False)
    plot.tools = [PanTool(dimensions=['width']), WheelZoomTool(dimensions=['width']), ResetTool(), PreviewSaveTool()]
    
    return components(plot, CDN)
