'''
Created on Feb 15, 2016

@author: Miguel Urco
'''

import json

def read_json_file(fp):
    
    kwargs = {}
    
    json_data = fp
    data = json.load(json_data)
    json_data.close()
    
    frequency0 = data["Frequencies"][0][1]
    frequency1 = data["Frequencies"][1][1]
    frequency2 = data["Frequencies"][2][1]
    frequency3 = data["Frequencies"][3][1]
    
    kwargs['freq0'] = frequency0
    kwargs['freq1'] = frequency1
    kwargs['freq2'] = frequency2
    kwargs['freq3'] = frequency3
    
    return kwargs


def write_json_file(filename):
    pass