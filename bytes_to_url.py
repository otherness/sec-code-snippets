#!/usr/local/bin/python


import requests,sys,base64,urllib,binascii


url_post = 'http://natas28.natas.labs.overthewire.org/index.php'
url_get = 'http://ptl-18151529-ed22e0cd.libcurl.so/index.php'
#cred = ('natas28', 'JWwR438wkgTsNKBbcJoowyysdM82YjeF')
#hdrs = {'Content-Type': 'application/x-www-form-urlencoded'}
prx = {
  'http': 'http://127.0.0.1:8080',
  'https': 'http://127.0.0.1:8080',
}

class bcolors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'

# print encrypted_msg_url_enc
# encrypted_msg_base64 = urllib.unquote(encrypted_msg_url_enc)
# encrypted_msg_ascii = base64.b64decode(encrypted_msg_base64)
# print binascii.hexlify(encrypted_msg_ascii)
#
# encrypted_msg = binascii.hexlify(encrypted_msg_ascii)
# n=0
# enc_msg_list = []

def xor_hex_str(str1,str2):
    assert len(str1)==len(str2)
    str1_hex = int(str1, 16)
    str2_hex = int(str2, 16)
    return str(format(str1_hex ^ str2_hex, '02x'))


def encode_payload(pld):
    payload_ascii = binascii.unhexlify(pld)
    payload_base64 = base64.b64encode(payload_ascii)
    return urllib.quote(payload_base64, safe ='')

def decode_answer(ans):
    ans_base64 = urllib.unquote(ans)
    ans_ascii = base64.b64decode(ans_base64)
    #print ans_base64
    return binascii.hexlify(ans_ascii)


def assemble_payload(index,modified_prev_block):
    payload = ""
    for i in range(0,index+1):
        if i == index-1:
            payload+=modified_prev_block
            continue
        payload+=enc_msg_list[i]
    return payload


#block is string in hex format XX without leading 0x
def divide_block_to_bytes(block):
    n = 2 #two chars for each byte
    print "Dividing block " + block
    block_byte_list = [block[i:i+n] for i in range (0, len(block), n)]
    return block_byte_list


def apply_padding_xor(byte_list, pad_size):
    xored_byte_list = byte_list[:-pad_size]
    print "DEBUG: Applying padding to block:", byte_list
    print "DEBUG: Padding size:", pad_size
    pad_size_str = str(format(pad_size, '02x')) #convert padding byte to string
    print "DEBUG: Padding in hex: " + pad_size_str
    print "DEBUG: Applying padding to last", pad_size, "bytes only:", byte_list[-pad_size:]
    for byte in byte_list[-pad_size:]:
        xored_byte_list.append(xor_hex_str(byte, pad_size_str))
    return xored_byte_list




def print_hex(string):
    base = 32
    for i in range (len(string)/32):
        if i%2 == 0:
            print bcolors.OKBLUE + string[base*i:base*(i+1)] + bcolors.ENDC,
        else:
            print bcolors.OKGREEN + string[base*i:base*(i+1)] + bcolors.ENDC,
    print

#input_list = ["A", "AA", "AAA", "AAAA", "AAAAA", "AAAAAA", "AAAAAAA",\
#"AAAAAAAA", "AAAAAAAAA", "AAAAAAAAAA", "AAAAAAAAAAA", "AAAAAAAAAAAA", "AAAAAAAAAAAAA", "AAAAAAAAAAAAAA", \
#"AAAAAAAAAAAAAAAAAAAAAAAA", "BBBBBBAAAAAAAAAAAAAAAAAAA", "BBBBBBBBBBAAAAAAAAAAAA", "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"]


# for guess in range (32,127):
#     query = "BBBBBBBBBBAAAAAAAAAAAAA" + urllib.quote(binascii.unhexlify(str(format(guess, '02x'))), safe='')
#     r = requests.post(url_post, auth = cred, proxies = prx, headers = hdrs, data = "query="+query, allow_redirects=False)
#     loc_header = r.headers['Location']
#     equal_sign_pos = loc_header.find('=') + 1
#     ans_hex = decode_answer(loc_header[equal_sign_pos:])
#     print binascii.unhexlify(str(format(guess, '02x'))), urllib.quote(binascii.unhexlify(str(format(guess, '02x'))), safe='')
#     print_hex(ans_hex)
#     ans_hex[96:128]
#     if ans_hex[96:128] == "8e59c7cc6f7a42392748b530014e125f":
#         print binascii.unhexlify(str(format(guess, '02x')))
#         break


hex_get_query = "b4048b360f86eb314c27ab705949a4f5"

#hex_get_query += "d8ae51d7da71b2b083d919a0d7b88b98" #append full block of PKCS#7 padding
payload = encode_payload(hex_get_query)
print payload
cookies = {'auth':payload}
#hdrs = {'Cookie:' : 'auth=' + encode_payload(hex_get_query)}
r = requests.get(url_get, cookies = cookies, proxies = prx)
print r.content


# post_query_hex = "f633e6b05f866226b863817112b1c92b"
# r = requests.post(url_post, auth = cred, proxies = prx, headers = hdrs, data = "query="+binascii.unhexlify(post_query_hex), allow_redirects=False)
# loc_header = r.headers['Location']
# equal_sign_pos = loc_header.find('=') + 1
# print decode_answer(loc_header[equal_sign_pos:])
