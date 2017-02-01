
import json


def parse_range(s):
    
    vars = ('TXA,', 'A,', 'TXB,', 'B,', 'TXA', 'TXB', 'A', 'B')
    
    for var in vars:
        if var in s:
            s = s.replace(var, '')
            if 'A' in var:
                ref = 'TXA'
            else:
                ref = 'TXB'
            return ref, s
        
    return '0', s
        

class RCFile(object):
    '''
    Class to handle Radar controller configuration files
    '''
    
    def __init__(self, f=None):
        
        self.data = {}
        self.line = ''
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
            elif 'json' in self.name:
                self.data = json.load(self.f)
        
        self.f.close()

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
        self.data['clock_in'] = float(data['RELOJ'])*self.data['clock_divider']
        self.data['clock'] = float(data['RELOJ'])
        self.data['time_before'] = int(data['TR_BEFORE'])
        self.data['time_after'] = int(data['TR_AFTER'])
        
        if 'SYNCHRO DELAY' in data:
            self.data['sync'] = int(data['SYNCHRO DELAY'])
        else:
            self.data['sync'] = 0
        self.data['lines'] = []

        if 'SAMPLING REFERENCE' in data:
            if data['SAMPLING REFERENCE']=='MIDDLE OF FIRST BAUD':
                self.data['sampling_reference'] = 'first_baud'
            elif data['SAMPLING REFERENCE']=='MIDDLE OF FIRST SUB-BAUD':
                self.data['sampling_reference'] = 'sub_baud'
            else:
                self.data['sampling_reference'] = 'none'                

        #Add TR line
        if 'Pulse selection_TR' in data:
            ref, rng = parse_range(data['Pulse selection_TR'])
            line = {'type':'tr', 'range': rng if rng else '0', 'TX_ref':ref}
        else:
            line = {'type': 'tr', 'range': '0', 'TX_ref': '0'}
        
        self.data['lines'].append(line)
        
        #Add TX's lines
        if 'TXA' in data:
            line = {'type':'tx', 'pulse_width':data['TXA'], 'delays':'0'}
            if 'Pulse selection_TXA' in data:
                line['range'] = data['Pulse selection_TXA']
            else:
                line['range'] = '0'
            self.data['lines'].append(line)
        else:
            self.data['lines'].append({'type':'tx', 'pulse_width':'0', 'delays':'0', 'range':'0'})
                    
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
        else:
            self.data['lines'].append({'type':'tx', 'pulse_width':'0', 'delays':'0', 'range':'0'})
        
        #Add Other lines (4-6)
        for n in range(4, 7):
            params = self.get_line_parameters(data, n)
            labels = params.keys()
            
            if 'L%d_FLIP' % n in labels:
                line = {'type':'flip', 'number_of_flips':data['L%d_FLIP' % n]}
            elif 'Code Type' in data and n==4:
                line = {'type':'codes', 'code':data['Code Type'], 'TX_ref':data['L%d_REFERENCE' % n]}
                if 'Number of Codes' in data:
                    line['codes'] = [data['COD({})'.format(x)] for x in range(int(data['Number of Codes']))]
            elif 'Code Type (Line %d)' % n in labels:
                line = {'type':'codes', 'code':data['Code Type (Line %d)' % n], 'TX_ref':data['L%d_REFERENCE' % n]}
                if 'Number of Codes (Line %d)' % n in data:
                    line['codes'] = [data['L{}_COD({})'.format(n, x)] for x in range(int(data['Number of Codes (Line %d)' % n]))]
            elif 'Sampling Windows (Line %d)' % n in data:
                line = {'type':'windows', 'TX_ref':data['L%d_REFERENCE' % n]}
                windows = []
                for w in range(int(data['Sampling Windows (Line %d)' % n])):
                    windows.append({'first_height':float(data['L%d_H0(%d)' % (n, w)]),
                         'resolution':float(data['L%d_DH(%d)' % (n, w)]),
                         'number_of_samples':int(data['L%d_NSA(%d)' % (n, w)]),
                         'last_height':float(data['L%d_DH(%d)' % (n, w)])*(int(data['L%d_NSA(%d)' % (n, w)])-1)+float(data['L%d_H0(%d)' % (n, w)])
                         }
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
                     'resolution':float(dh),
                     'last_height':float(h0)+float(dh)*(int(nsa)-1)}
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


