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
module_xx = ('192.168.1.xx',5500)

@route('/')
@route('/hello')
def hello():
    return "Hello World!"


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
    try:
        header_rx = request.forms.get('header')
        module_rx = request.forms.get('module')
        beams_rx  = request.forms.get('beams')
        beams_rx  = json.loads(beams_rx)
    except:
        return {"status":0, "message": "Could not accept configuration"}
    #print header_rx, module_rx, beams_rx
    message_tx = header_rx+"\n"+module_rx+"\n"
    for i in range(1,len(beams_rx)+1):
        message_tx = message_tx+beams_rx[str(i)]+"\n"
    message_tx = message_tx+"0"

    # Create the datagram socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print >>sys.stderr, 'sending "%s"' % message_tx
    sock.connect(module_63)
    sock.send(message_tx)
    sock.close()

    return {"status":1, "message": "Configuration has been successfully sent"}

@error(404)
def error404(error):
    return "^^' Nothing here, try again."

run(host=module_ip, port=8080, debug=True)
