import json
from hashlib import sha256
from time import time
from flask import Flask, jsonify, request
import requests
import threading
import random
app = Flask(__name__)














name = ""
___port = 5000


blockchain = {}
lastBlockHash = ""

blockSize = 1


newBlock = {}

memoryPool = []


@app.route("/addEntry", methods=['POST'])
def addEntry():

    data = request.form
    hash =  data.get("hash")
    timestamp = data.get("timestamp")
    type = data.get("type")
    author = data.get("author")

    entry = {"hash": hash,
             "timestamp": timestamp,
             "type": type,
             "author": author}

    memoryPool.append(entry)
    return "Done"


@app.route("/show", methods=['GET'])
def showEntries():
    return json.dumps(blockchain)

class Miner (threading.Thread):

    def __init__(self):
      threading.Thread.__init__(self)

    def run(self):
        global blockchain
        global newBlock
        global lastBlockHash
        global blockSize
        global name

        while True:

            while len(memoryPool) < blockSize:
                continue

            newBlock = {}

            for i in range(blockSize):
                newBlock["entries"] = []
                newBlock["entries"].append(memoryPool.pop(i))

            newBlock["timestamp"] = time() 
            newBlock["last"] = lastBlockHash
            newBlock["autority"] = name

            # Défi
            newBlock["nounce"] = random.randint(0, 999999999)
            hash = sha256(json.dumps(newBlock).encode("utf-8")).hexdigest()
            while hash[0:4] != "0000":

                newBlock["nounce"] += 1
                hash = sha256(json.dumps(newBlock).encode("utf-8")).hexdigest()
            
            lastBlockHash = hash
            blockchain[hash] = newBlock



if __name__ == '__main__':

    miner = Miner()
    miner.start()

    app.run(host='127.0.0.1', port=5000)   
    
