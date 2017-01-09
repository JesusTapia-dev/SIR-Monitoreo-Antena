"""
This script should run in the absmodule.
"""
import socket
import struct
import sys

multicast_group = '224.3.29.71'
server_address = ('',10000)

absmod = ('10.10.20.53', 5500) #This IP should be modificated according to its absmodule
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(absmod)

# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the server address
sock.bind(server_address)

#Tell the operating system to add the socket to the multicast group
#on all interfaces.
group = socket.inet_aton(multicast_group)
mreq  = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
#Receive/respond loop

while True:

    print >>sys.stderr, '\nwaiting to receive message'
    data, address = sock.recvfrom(1024)
    if data != '':
        message = data
        
        s.sendto(message,absmod)
        rx_text = s.recv(1024)
        s.close()
        s = None
        print >>sys.stderr, 'Respond from TCP server: %s' % rx_text
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(absmod)
        except:
            print '\nProblem with creating socket repeater!!...\n'
            s.close()
            s = None
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(absmod)
            break

    print >>sys.stderr, 'received %s bytes from %s' % (len(data), address)
    print >>sys.stderr, data

    #print >>sys.stderr, 'sending acknowledgement to', address
    #sock.sendto('ack', address)break
