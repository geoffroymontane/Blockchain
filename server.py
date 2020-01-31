import json
from hashlib import sha256
from time import time as getTime
from flask import Flask, jsonify, request
from math import floor
import requests
import threading
import random
import sys
app = Flask(__name__)













name = ""
___ip = ""
___port = 0


neighbors = []

blockchain = {}
entriesHash = []
lastBlockHash = ""

blockSize = 3

miningSafe = True

newBlock = {}

memoryPool = {}


miner = ""


def time():
    return floor(getTime())



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
    currentAvgTimestamp = avgTimestamp(blockchain[root]) // 2
    length = 1

    correct = True
    while True: 
        hasAParent = False
        for hash in blockchain:
            if blockchain[hash]["last"] == current:
                current = hash

                correct = correct and checkBlock(current, blockchain[current])
                correct = correct and avgTimestamp(blockchain[current]) > currentAvgTimestamp

                currentAvgTimestamp = expoAvgTimestamp(currentAvgTimestamp, blockchain[current])
                length += 1
            
                hasAParent = True
                break
        if not hasAParent:
            break

    correct = correct and (length == len(blockchain))


    print(correct)
    print(length)
    return correct, length

class Miner (threading.Thread):

    def __init__(self):
      threading.Thread.__init__(self)

    def stop(self):
        self._stop_event.set()

    def run(self):
        global blockchain
        global newBlock
        global lastBlockHash
        global blockSize
        global name

        while True:
            
            while len(memoryPool) < blockSize:
                continue

            if not miningSafe:
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

            if not miningSafe:
                continue

            # Défi
            newBlock["nounce"] = random.randint(0, 999999999)
            hash = sha256(json.dumps(newBlock).encode("utf-8")).hexdigest()
            while hash[0:5] != "00000" and miningSafe:

                newBlock["nounce"] += 1
                hash = sha256(json.dumps(newBlock).encode("utf-8")).hexdigest()

            if not miningSafe:
                continue

            for block in blockchain:
                for entry in blockchain[block]["entries"]:
                    if entry in entriesHash:
                        continue
            
            lastBlockHash_ = hash
            blockchain[hash] = newBlock

            for entry in newBlock["entries"]:
                entriesHash.append(entry["hash"])

            print("----")
            print("Mined")
            print("----")

            for neighbor in neighbors:
                ip = str(neighbor["ip"])
                port = str(neighbor["port"])
                r = requests.post(url = "http://" + ip + ":" + port + "/submitBlockchain",
                json = blockchain)

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

        for neighbor in neighbors:
            ip = str(neighbor["ip"])
            port = str(neighbor["port"])
            r = requests.post(url = "http://" + ip + ":" + port + "/addEntry",
            data = {"hash": hash}) 

        print("----")
        print("New entry: ")
        print(str(len(memoryPool)) + " / " + str(blockSize))
        print("----")

        return "Done"

    return "Error"


@app.route("/show", methods=['GET'])
def showEntries():
    return json.dumps(blockchain)


@app.route("/submitBlockchain", methods=['POST'])
def submitBlockchain():
    global blockchain
    blockchain_ = request.json  

    print("New blockchain received") 

    check = checkBlockchain(blockchain_)
    if check[0] and check[1] > len(blockchain):
        miningSafe = False
        print("Blockchain switching...") 

        blockchain = blockchain_ 

        # Trouver la racine
        for hash in blockchain:
            if blockchain[hash]["last"] == "":
                root = hash
                break

        current = root
        while True: 
            hasAParent = False
            for entry in blockchain[current]["entries"]:
                entriesHash.append(entry["hash"])
            for hash in blockchain:
                if blockchain[hash]["last"] == current:
                    current = hash
                    hasAParent = True
            if not hasAParent:
                break

        lastBlockHash = current

        memoryPool = {}
        newBlock = {}

        miningSafe = True
        return "Done"

    return "Error"

if __name__ == '__main__':

    ___ip = input("IP : ")
    ___port = input("Port : ")


    neighbors = [{"ip": input("Voisin IP : "), "port": input("Voisin Port: ")}]


    miner = Miner()
    miner.start()

    app.run(host=___ip, port = ___port)   
    
