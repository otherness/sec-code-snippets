#!/usr/local/bin/python
import base64


def sxor(s1,s2):
    # convert strings to a list of character pair tuples
    # go through each tuple, converting them to ASCII code (ord)
    # perform exclusive or on the ASCII code
    # then convert the result back to ASCII (chr)
    # merge the resulting array of characters as a string
    return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))

st = '{"showpassword":"no","bgcolor":"#ffffff"}'
target = "ClVLIh4ASCsCBE8lAxMacFMZV2hdVVotEhhUJQNVAmhSEV4sFxFeaAw="

print st
print target



result = base64.b64decode(target)
print result


#secr = sxor(st, result)
secr = 'qw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8J'


new_value = '{"showpassword":"yes","bgcolor":"#ffffff"}'
print base64.b64encode(sxor(new_value,secr))

print "Check:"

check = sxor(base64.b64decode('ClVLIh4ASCsCBE8lAxMacFMOXTlTWxooFhRXJh4FGnBTVF4sFxFeLFMK'),secr)

print check
#for i in range(0,64):
#    print base64.b64encode(first_symbol ^ i)
