from hashlib import sha256
from datetime import datetime
from time import time
import sys
import requests
import json
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

def run():
    global filename
    global author
    global type

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


def verification():
    global filename
    global author
    global type
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
    print("Hash : " + hash)

    date = 0
    text = requests.get(url = "http://localhost:5000/show").text
    blockchain = json.loads(text)

    for block in blockchain:
        for transaction in blockchain[block]['entries']:
            if (transaction['hash'] == hash):
                date = transaction['timestamp']
                print("Copyright in ", datetime.fromtimestamp(date))
                str_ = "Copyright in " + str(datetime.fromtimestamp(date))
                return str_
                break
        if (date != 0):
             break
        print('No copyright registered')
        return ('No copyright registered')

    print("end")




