import json
from hashlib import sha256
from time import time as getTime
from flask import Flask, jsonify, request
from math import floor
import requests
import threading
import random
app = Flask(__name__)














name = ""
___port = 5000


blockchain = {}
entriesHash = []
lastBlockHash = ""

blockSize = 3


newBlock = {}

memoryPool = {}


def time():
    return floor(getTime())


#
# API
#

@app.route("/addEntry", methods=['POST'])
def addEntry():

    data = request.form
    hash =  data.get("hash")

    if hash not in memoryPool and hash not in entriesHash:

        entry = {"hash": hash, "timestamp": time()}

        memoryPool[hash] = entry

        print("----")
        print("New entry: ")
        print(str(len(memoryPool)) + " / " + str(blockSize))
        print("----")

        return "Done"

    return "Error"


@app.route("/show", methods=['GET'])
def showEntries():
    return json.dumps(blockchain)



#
#
#

def checkBlock(hash, block):
    return sha256(json.dumps(block).encode("utf-8")).hexdigest() == hash


def avgTimestamp(block):

    sum = 0
    for entry in block["entries"]:
       sum += entry["timestamp"] 

    sum //= len(block["entries"])

    return sum

def expoAvgTimestamp(avg, block):
    sum = avgTimestamp(block) 
    return 0.9 * avg  + 0.1 * sum


def checkBlockchain(blockchain):

    # Trouver la racine
    for hash in blockchain:
        if blockchain[hash]["last"] == "":
            root = hash
            break

    # Remonter la chaîne en vérifiant les hash et les timestamps
    current = root
    currentAvgTimestamp = avgTimestamp(root) // 2
    length = 1

    correct = True
    while True: 
        for hash in blockchain:
            if blockchain[hash]["last"] == current:
                current = hash

                correct = correct and checkBlock(current, blockchain[current])
                correct = correct and avgTimestamp(current) > currentAvgTimestamp

                currentAvgTimestamp = expoAvgTimestamp(currentAvgTimestamp, current)
                length += 1

                if not correct:
                    return False

    correct = correct and length = len(blockchain)


    return correct, length

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

            print("----")
            print("Mining...")
            print("----")

            newBlock = {}
            memoryPoolKeys = list(memoryPool.keys())
            newBlock["entries"] = []
            for i in range(blockSize):
                newBlock["entries"].append(memoryPool.pop(memoryPoolKeys[i]))
            random.shuffle(newBlock["entries"])

            newBlock["timestamp"] = time() 
            newBlock["last"] = lastBlockHash
            newBlock["autority"] = name

            # Défi
            newBlock["nounce"] = random.randint(0, 999999999)
            hash = sha256(json.dumps(newBlock).encode("utf-8")).hexdigest()
            while hash[0:5] != "00000":

                newBlock["nounce"] += 1
                hash = sha256(json.dumps(newBlock).encode("utf-8")).hexdigest()
            
            lastBlockHash = hash
            blockchain[hash] = newBlock

            for entry in newBlock["entries"]:
                entriesHash.append(entry["hash"])

            print("----")
            print("Mined")
            print("----")


if __name__ == '__main__':

    miner = Miner()
    miner.start()

    app.run(host='127.0.0.1', port=5000)   
    
