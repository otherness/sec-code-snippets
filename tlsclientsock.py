#!/usr/bin/python

import sys
import socket, ssl, time

#print "First argument is " + str(sys.argv[1])
host = sys.argv[1]
port = 443
httpget = "HEAD / HTTP/1.1\r\nHost: " + str(host) + "\r\nConnection: Close\r\n\r\n"

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)

sslsock = context.wrap_socket(sock, server_hostname=host)

sslsock.connect((host,port))

#sslsock.write(b'HEAD / HTTP/1.1\r\n')
sslsock.sendall(httpget)

#print(sslsock.recv().decode())
#s.sendall(httpget)
resp = sslsock.recv(4096)
print resp
time.sleep(30)
sslsock.close()
sock.close()
