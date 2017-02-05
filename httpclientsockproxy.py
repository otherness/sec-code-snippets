#!/usr/bin/python

import sys
import socket

#print "First argument is " + str(sys.argv[1])
host = sys.argv[1]
httpget = "GET http://" + str(host) + "/ HTTP/1.1\r\nHost: " + str(host) + "\r\nConnection: keep-alive\r\n\r\n"
print httpget

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('127.0.0.1',8080))
s.sendall(httpget)
resp = s.recv(4096)
s.close()

print resp