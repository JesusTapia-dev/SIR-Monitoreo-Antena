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
        print 'RC Configuration: {}'.format(self.params['name'])
        
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
        url_divider = os.path.join(self.url, 'divisor')
                
        values = zip(self.params['pulses'], 
                     [x-1 for x in self.params['delays']])
        payload = ''
        
        for tup in values:
            vals = pack('<HH', *tup)
            payload += '\x05'+vals[0]+'\x04'+vals[1]+'\x05'+vals[2]+'\x04'+vals[3]
        
        req = requests.post(url_divider, 
                            data={'divisor':int(self.params['clock_divider'])-1})
        
        if 'ok' not in req.text:
            print 'Error sending divider'
            return False
        
        req = requests.post(url_write, 
                            data=b64encode(payload))
        return req.json()

if __name__ == '__main__':
    
    ip = '10.10.10.100'    
    filename = '/home/jespinoza/Downloads/rc_150EEJ.json'    

    rc = RCApi(ip)
    rc.load(filename)
    
    print rc.status()
    print rc.reset()
    print rc.stop()
    print rc.write()
    print rc.start()
    
    
    



