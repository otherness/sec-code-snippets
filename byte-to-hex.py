#!/usr/local/bin/python

byte_list = [['09', '09', '09', '09', '09', '09', '09', '09', '09', '09', '09', '09', '09', '09', '09', '09'], ['54', '68', '65', '20', '4d', '61', '67', '69', '63', '20', '57', '6f', '72', '64', '73', '20']]

byte_list.reverse()
print "ANSWER in hex:", byte_list
#convert byte array to string
ans_string = ""
for block in byte_list:
    for byte in block:
        ans_string+=byte

print "ANSWER in ASCII:", ans_string.decode('hex')
