"""
This script should run in the abs module embedded system
It creates a Web Application with API Restful Bottle to connect to SIR server.
It needs the following scripts: abs_gpio.py and bottle.py
"""
from bottle import route, run, request
from bottle import error
from abs_gpio import abs_read

#Sockets
import socket
import sys

import json

module_ip  = '192.168.1.xx'
module_num = 'xx'
module_port = 5500
module = (module_ip,5500)

#This function decode sent characters
def fromChar2Binary(char):
    #To get the real value (-33)
    number = ord(char) - 33
    bits = bin(number)[2:]
    #To ensure we have a string with 6bits
    if len(bits) < 6:
        bits = bits.zfill(6)
    return bits

@route('/')
@route('/hello')
def hello():
    return "Hello World!"

"""
#---- Send Bits Function ----
@route('/write', method='POST')
def writebits():

    #This funcion configure ABS sending bits.

    try:
        #------------Get Values-----------
        #----------------UP---------------
        ub2     = request.forms.get('ub2')
        ub1     = request.forms.get('ub1')
        ub0     = request.forms.get('ub0')
        #--------------DOWN---------------
        db2     = request.forms.get('db2')
        db1     = request.forms.get('db1')
        db0     = request.forms.get('db0')

        #-----------Send Values-----------
        #----------------UP---------------
        ub2 = abs_write(126,ub2)
        ub1 = abs_write(124,ub1)
        ub0 = abs_write(122,ub0)
        #--------------DOWN---------------
        db2 = abs_write(120,db2)
        db1 = abs_write(118,db1)
        db0 = abs_write(116,db0)

        if (ub2+ub1+ub0+db2+db1+db0) == 6:
            return {"status": 1, "message": "Bits were successfully adjusted"}
        else:
            return {"status": 0, "message": "Couldn't configure ABS"}

    except:
        return {"status": 0, "message": "Couldn't configure ABS"}
"""

#------ Get Status -------                                                    
@route('/status', method='GET')                                               
def module_status():                                                          
    """                                                                       
    This function returns:                                                    
    0 : No Connected                                                          
    1 : Connected                                                             
                                                                              
    """                                                                       
    message_tx = 'JROABSClnt_01CeCnMod000001MNTR10'                           
    #Create the datagram socket                                               
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                  
    try:                                                                      
        sock.connect(module)                                                  
        sock.send(message_tx)                                                 
        sock.close()                                                          
    except:                                                                   
        sock = None                                                           
        return {"status":0, "message": "TCP Control Module not detected."}    
    return {"status": 1, "message": "Module "+module_num+" is running"} 


#---- Get Bits Function ----
@route('/read', method='GET')
def readbits():

    """
    This function reads the real values from the embedded system pins
    with gpio class
    """

    #This function reads sent bits.

    #------Get Monitoring Values------
    #----------------UP---------------
    um2_value = abs_read(80) #(++)
    um1_value = abs_read(82)
    um0_value = abs_read(84) #(--)
    #--------------DOWN---------------
    dm2_value = abs_read(94) #(++)
    dm1_value = abs_read(88)
    dm0_value = abs_read(86) #(--)

    allbits = [um2_value, um1_value, um0_value, dm2_value, dm1_value, dm0_value]
    if "" not in allbits:
        allbits = {"um2":int(um2_value), "um1": int(um1_value), "um0": int(um0_value), "dm2": int(dm2_value), "dm1": int(dm1_value), "dm0": int(dm0_value)}
        #allbits = {"ub0":0, "ub1":0, "ub2":0, "db0":0, "db1":0, "db2":0}
        return {"status": 1, "message": "Bits were successfully read", "allbits" : allbits}
    else:
        return {"status": 0, "message": "There's a problem reading bits", "allbits" : ""}

@route('/write', method='POST')
def writebits():
    """
    This function sends configurations to the module tcp_
    """
    header_rx = 'JROABSCeCnModCnMod01000108SNDFexperimento1.ab1'
    module_rx = 'ABS_'+module_num
    try:
        #header_rx = request.forms.get('header')
        #module_rx = request.forms.get('module')
        #beams_rx  = request.forms.get('beams')
        #beams_rx  = json.loads(beams_rx)
        beams_rx  = json.loads(request.body.readline())
        beams_rx  = beams_rx['beams']
    except:
        return {"status":0, "message": "Could not accept configuration"}
    #print beams_rx
    message_tx = header_rx+"\n"+module_rx+"\n"
    for i in range(0,len(beams_rx)): #(1,len(beams_rx)+1)
        try:
            message_tx = message_tx+fromChar2Binary(beams_rx[i])+"\n"
        except:
            return {"status":0, "message": "Error in parameters from Beams List"}
    message_tx = message_tx+"0"


    # Create the datagram socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print >>sys.stderr, 'sending "%s"' % message_tx
    sock.connect(module)
    sock.send(message_tx)
    sock.close()

    return {"status":1, "message": "Configuration has been successfully sent"}

@error(404)
def error404(error):
    return "^^' Nothing here, try again."

run(host=module_ip, port=8080, debug=True)
