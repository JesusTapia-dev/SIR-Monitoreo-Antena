"""
This script should run in SIR. It creates a multicast server.
This server connects SIR client to a absmodule socket. SIR client socket sends SIR data to multicast server. This server sends the data to a
absmodule socket repeater that re-sends the configuration to Tcp Control Module (C server running in absmodule).
"""

import socket
import struct
import sys

#-------Socket Server----------
sock_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock_server.bind(('',4242))
mreq = struct.pack("=4sl", socket.inet_aton("224.3.29.71"),socket.INADDR_ANY)
sock_server.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

while True:
    print sock_server.recv(1024)
