#!/usr/bin/python

import sys
import socket

#print "First argument is " + str(sys.argv[1])
host = sys.argv[1]
port = 80
httpget = "GET / HTTP/1.1\r\nHost: " + str(host) + "\r\nConnection: Close\r\n\r\n"
print httpget

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((host,port))
s.sendall(httpget)
resp = s.recv(4096)
s.close()

print resp
