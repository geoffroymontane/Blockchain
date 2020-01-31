from hashlib import sha256
from time import time
import sys
import requests
from GUI import *

author = ''
filename = ''
type = ''

def storeString1(inString):
    global author
    author = inString
    # Do something with the string
    print('Author is: ',author)
    return

def storeString2(inString):
    global filename
    filename = inString
    # Do something with the string
    print('filename is: ',filename)
    return

def storeString3(inString):
    global type
    type = inString
    # Do something with the string
    print('type is: ',type)
    return
print('phase 1')
get_values()
print('phase 2')
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

# Hash typeleo
typeHash = sha256(type.encode("utf-8")).hexdigest()

# Hash
hash = sha256((fileHash + authorHash + type).encode("utf-8")).hexdigest()


# Request
print("Hash : " + hash)
r = requests.post(url = "http://localhost:5000/addEntry", data = {"hash": hash}) 
print(r.text)
