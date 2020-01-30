from hashlib import sha256
from time import time
import sys
import requests




filename = sys.argv[0]
author = sys.argv[1]
type = sys.argv[2]

# Hash the file
h  = sha256()
b  = bytearray(128*1024)
mv = memoryview(b)
with open(filename, 'rb', buffering=0) as f:
    for n in iter(lambda : f.readinto(mv), 0):
        h.update(mv[:n])
fileHash = h.hexdigest()



# Hash author name
authorHash = sha256(author.encode("utf-8")).hexdigest()

# Hash type
typeHash = sha256(type.encode("utf-8")).hexdigest()

# Hash
hash = sha256((fileHash + authorHash + type).encode("utf-8")).hexdigest()


# Request
print("Hash : " + hash)
r = requests.post(url = "http://localhost:5000/addEntry", data = {"hash": hash}) 
print(r.text)
