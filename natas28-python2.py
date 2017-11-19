import requests
from urllib import quote, unquote
import re

natas_url = "http://natas28.natas.labs.overthewire.org/index.php"
search_url = "http://natas28.natas.labs.overthewire.org/search.php/?query="

#authorization header
headers = {"Authorization": "Basic bmF0YXMyODpKV3dSNDM4d2tnVHNOS0JiY0pvb3d5eXNkTTgyWWplRg=="}

log.info("Retrieving first ciphertext")

#pad plaintext to ensure it takes up a full ciphertext block
plaintext = "A"*10 + "B"*14
resp = requests.post(natas_url, data={"query": plaintext}, headers=headers)

#get the raw bytes of the ciphertext
encoded_ciphertext = resp.url.split("query=")[1]
ciphertext = unquote(encoded_ciphertext).decode("base64")

print ciphertext
