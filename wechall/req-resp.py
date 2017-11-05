#!/usr/bin/env python

import requests

url = 'https://www.wechall.net/challenge/training/programming1/index.php?action=request'
hdrs = {"Cookie": "WC=9947200-37744-oAEN4l4C9SjNtXub"}
r = requests.get(url, headers=hdrs)

url2 = 'https://www.wechall.net/challenge/training/programming1/index.php?answer=' + r.text

r2 = requests.get(url2, headers=hdrs)
print(r2.text)
