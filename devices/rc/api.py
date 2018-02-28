'''
API to configure new Radar controller


@author: Juan C. Espinoza
'''

import os
import json
import requests
from struct import pack
from base64 import b64encode

class RCApi(object):
    
    def __init__(self, ip, port=80):
        
        self.url = 'http://{}:{}/'.format(ip, port)
        self.params = None        

    def load(self, filename):
        
        self.params = json.load(open(filename))
        self.pk = self.params['configurations']['allIds'][0]      
        print 'RC Configuration: {}'.format(self.params['configurations']['byId'][self.pk]['name'])
        
    def status(self):
        
        url = os.path.join(self.url, 'status')
        req = requests.get(url)
        return req.json()

    def read(self):
        
        url = os.path.join(self.url, 'read')
        req = requests.get(url)
        return req.json()

    def stop(self):
        
        url = os.path.join(self.url, 'stop')
        req = requests.post(url)
        return req.json()

    def reset(self):
        
        url = os.path.join(self.url, 'reset')
        req = requests.post(url)
        return req.json()

    def start(self):
        
        url = os.path.join(self.url, 'start')
        req = requests.post(url)
        return req.json()
    
    def write(self):
        
        url_write = os.path.join(self.url, 'write')
        url_divider = os.path.join(self.url, 'divider')            

        values = zip(self.params['configurations']['byId'][self.pk]['pulses'], 
                     [x-1 for x in self.params['configurations']['byId'][self.pk]['delays']])
        payload = ''
        
        for tup in values:
            vals = pack('<HH', *tup)
            payload += '\x85'+vals[0]+'\x84'+vals[1]+'\x85'+vals[2]+'\x84'+vals[3]
        
        req = requests.post(url_divider, 
                            data={'divider':int(self.params['configurations']['byId'][self.pk]['clock_divider'])-1})
                
        if 'ok' not in req.text:
            print 'Error sending divider'
            return False

        req = requests.post(url_write, 
                            data=b64encode(payload))
        return req.json()

if __name__ == '__main__':
    import time
    ip = '10.10.10.100'    
    
    filename = './dia.json'    
    
    rc = RCApi(ip)
    rc.load(filename)
    
    # print rc.status()
    # time.sleep(1)
    # print rc.reset()
    # time.sleep(1)
    # print rc.stop()
    # time.sleep(1)
    print rc.write()
    # time.sleep(1)
    # print rc.start()
    
    
    



