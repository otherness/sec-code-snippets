#!/usr/bin/python

import sys
import httplib
import ssl

#print "First argument is " + str(sys.argv[1])
con = httplib.HTTPSConnection(str(sys.argv[1]), timeout=5, context=ssl._create_unverified_context())
con.request("GET", "/")
resp = con.getresponse()
print resp.status, resp.reason
print resp.read()