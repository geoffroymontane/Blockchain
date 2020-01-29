import json
import hashlib
import json
from time import time
from hashlib import sha256

import threading

import random

import time

from flask import Flask
app = Flask(__name__)


blockchain = []
lastBlock = ""
transactionsUsed = []

transactionsBuffer = {}
newBlock = {}
blockSize = 1


___publicKey = ""
___privateKey = ""


___name = "Geoffroy<3"


@app.route("/", methods=['GET'])
def index():
    return "Coucou"

@app.route("/addTransaction", methods=['POST'])
def addTransaction():

    transaction = JSON.parse(request.form["data"])

    # Vérifie la signature de la transaction
    if checkSignature(sha256(request.form["data"]), transaction["signature"], transaction["publickey"]):

        # Check input transactions
        if "inputTransactions" not in transaction.keys():
            return "Error"

        inputAmount = 0
        for inputTransaction in transaction["inputTransactions"]:
            
            # Vérifier que ces inputTransactions existent
            if inputTransaction["hash"] in blockchain[inputTransactions["block"]]["transactions"]:

                # Vérifier que le commanditaire est bien bénéficiaire des inputTransactions
                if blockchain[inputTransactions["block"]]["transactions"][inputTransaction["hash"]]["publicKeyRecipient"] == transaction["publicKey"]:

                    # Vérifier que ces inputTransactions ne sont pas déjà utilisées
                    if inputTransaction["hash"] not in transactionsUsed: 

                        # Ajout du montant de l'inputTransaction au montant global
                        inputAmount += blockchain[inputTransactions["block"]]["transactions"][inputTransaction["hash"]]["amount"]
                    else:
                        return "Error"
                else:
                    return "Error"

            else:
                return "Error"

            
        if transaction["amount"] < 0:
            return "Error"

        # Si le montant en entrée est supérieur ou égal au montant de la transaction
        if inputAmount >= transaction["amount"]:

            transactionsBuffer[sha256(JSON.dumps(transaction))] = transaction

            # Noter les transactions utilisées
            for inputTransaction in transaction["inputTransactions"]:
                transactionsUsed.append(inputTransaction["hash"])


            # S'il reste une part du montant en entrée, créer une autre transaction du commanditaire à lui-meme
            remaining = inputAmount - transaction["amount"]
            if remaining != 0:

                remainingTransaction["signature"] = "NULL";
                remainingTransaction["timestamp"] = time.time();
                remainingTransaction["publicKey"] = transaction["publicKey"];
                remainingTransaction["publicKeyRecipient"] = transaction["publicKey"];
                remainingTransaction["amount"] = remaining;
                remainingTransaction["inputTransactions"] = transaction["inputTransactions"];

                transactionsBuffer[sha256(JSON.dumps(remainingTransaction))] = remainingTransaction
       
        else:
            return "Error"



class Scheduler (threading.Thread):
    def __init__(self):
      threading.Thread.__init__(self)

    def run(self):

        while len(transactionsBuffer) < blockSize:
            continue


        for i in range(blockSize):
            newBlock["transactions"] = []
            newBlock["transactions"][transactionsBuffer.keys()[i]] = transactionsBuffer.pop(transactionsBuffer.keys()[i])

        newBlock["timestamp"] = time.time() 
        newBlock["lastBlock"] = lastBlock
        newBlock["author"] = ___name
            
        newBlock["nounce"] = random.randint(0, 999999999)
        hash = sha256(str(JSON.dumps(newBlock)).encode("utf-8")).hexdigest()
        while hash[0:5] != "00000":
            newBlock["nounce"] += 1
            hash = sha256(str(JSON.dumps(newBlock)).encode("utf-8")).hexdigest()

        
        

        lastBlock = newBlock["hash"]




if __name__ == '__main__':

    scheduler = Scheduler()
    scheduler.start()

    app.run(host='127.0.0.1', port=5000)   
    
