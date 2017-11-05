#!/usr/local/bin/python

# Question 1
# In this project you will experiment with a padding oracle attack against a toy web site hosted at crypto-class.appspot.com.
# Padding oracle vulnerabilities affect a wide variety of products, including secure tokens.
# This project will show how they can be exploited. We discussed CBC padding oracle attacks in Lecture 7.6, but if you want to read more about them, please see Vaudenay's paper.
#
# Now to business. Suppose an attacker wishes to steal secret information from our target web site crypto-class.appspot.com.
# The attacker suspects that the web site embeds encrypted customer data in URL parameters such as this:
# http://crypto-class.appspot.com/po?er=f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4
# That is, when customer Alice interacts with the site, the site embeds a URL like this in web pages it sends to Alice.
# The attacker intercepts the URL listed above and guesses that the ciphertext following the "po?er=" is a hex encoded AES CBC encryption
# with a random IV of some secret data about Alice's session.
#
# After some experimentation the attacker discovers that the web site is vulnerable to a CBC padding oracle attack.
# In particular, when a decrypted CBC ciphertext ends in an invalid pad the web server returns a 403 error code (forbidden request).
# When the CBC padding is valid, but the message is malformed, the web server returns a 404 error code (URL not found).
#
# Armed with this information your goal is to decrypt the ciphertext listed above. To do so you can send arbitrary HTTP requests to the web site of the form
# http://crypto-class.appspot.com/po?er="your ciphertext here"
# and observe the resulting error code. The padding oracle will let you decrypt the given ciphertext one byte at a time.
# To decrypt a single byte you will need to send up to 256 HTTP requests to the site. Keep in mind that the first ciphertext block is the random IV.
# The decrypted message is ASCII encoded.
#
# To get you started here is a short Python (http://spark-university.s3.amazonaws.com/stanford-crypto/projects/pp4-attack_py.html) script that sends a ciphertext supplied on the command line to the site and prints the resulting error code.
# You can extend this script (or write one from scratch) to implement the padding oracle attack. Once you decrypt the given ciphertext, please enter the decrypted message in the box below.

# This project shows that when using encryption you must prevent padding oracle attacks by either using encrypt-then-MAC as in EAX or GCM,
# or if you must use MAC-then-encrypt then ensure that the site treats padding errors the same way it treats MAC errors.


import requests,sys,base64


url = 'http://crypto-class.appspot.com/po?er='
prx = {
  'http': 'http://127.0.0.1:8080',
  'https': 'http://127.0.0.1:8080',
}

block_size = 16
decrypted_msg = ""
encrypted_msg = "f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4"
n=0
enc_msg_list = []
guessed_list = []

def xor_hex_str(str1,str2):
    assert len(str1)==len(str2)
    str1_hex = int(str1, 16)
    str2_hex = int(str2, 16)
    return str(format(str1_hex ^ str2_hex, '02x'))


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



def xor_guess_and_guessed_bytes(g, ind, pad_prev_block, guessed_block):
    guess_xored_list = pad_prev_block[:]
    print "DEBUG: XOR with guess", g, "on position", ind, "to padded block", pad_prev_block
    guess_xored_list[ind] = xor_hex_str(g, pad_prev_block[ind])
    #print "DEBUG: Result after guess applied:", guess_xored_list
    #print "DEBUG: XOR with previously guessed ", guessed_block
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
print enc_msg_list

guessed_blocks_list_reverse = []
#iterating by block from last to first, index - actual index in block list
for index,enc_block in reversed(list(enumerate(enc_msg_list))):
    if index == 0:
        print "DEBUG: This is IV block"
        print "DEBUG: " + enc_block

    else:
        print("Guessing block number " + str(index+1) + ": " + enc_block)
        #divide previous block to bytes
        guessed_block = ["00"] * 16 # initialize guessed_block with all bytes = x00
        prev_block = enc_msg_list[index-1]
        prev_block_list=divide_block_to_bytes(prev_block)
        print "DEBUG: Previous block list: ", prev_block_list
        #iterate from last byte to first in previous block
        for byte_index in range(block_size-1, -1, -1):
            padding_size = block_size - byte_index #padding size depends on iteration number: 0x01, 0x0202, 0x030303, etc
            #print prev_block_list[byte_index:]
            padded_prev_block = apply_padding_xor(prev_block_list, padding_size)
            print "DEBUG: Prev block with applied padding:", padded_prev_block
            print "===================================================="
            #guessing byte with index byte_index
            for guess in range(0,256):
                prev_block_payload_list = xor_guess_and_guessed_bytes(str(format(guess, '02x')), byte_index, padded_prev_block, guessed_block)
                #convert prev_block_payload_list to string
                prev_block_payload = ""
                for byte in prev_block_payload_list:
                    prev_block_payload+=byte
                #print "DEBUG: String payload block:", prev_block_payload
                payload = assemble_payload(index,prev_block_payload)
                print "DEBUG: Full payload:",payload
                r = requests.get(url + payload, proxies=prx)
                print "DEBUG: STATUS CODE:", r.status_code
                if r.status_code == 200:
                    candidate_guess = str(format(guess, '02x'))
                if r.status_code == 404:
                    guessed_block[byte_index] = str(format(guess, '02x'))
                    print "\n================DEBUG: GUESSED byte",guessed_block,"\n===================="
                    break
                if guess == 255: # last iteration, no 404 were observed, going with candidate guess
                    guessed_block[byte_index] = candidate_guess
                    print "\n================DEBUG: NO 404 CODE, USED CANDIDATE GUESS, GUESSED byte",guessed_block,"\n===================="

        guessed_blocks_list_reverse.append(guessed_block)
        print "RESULT SO FAR:", guessed_blocks_list_reverse

guessed_blocks_list_reverse.reverse()

print "ANSWER in hex:", guessed_blocks_list_reverse

ans_string = ""
for block in guessed_blocks_list_reverse:
    for byte in block:
        ans_string+=byte

print "ANSWER in ASCII:", ans_string.decode('hex')
