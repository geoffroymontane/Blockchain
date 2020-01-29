from flask import Flask















___name = ""
___port = 5000



newBlock = {}

memoryPool = []


@app.route("addEntry", methods=['POST'])
def addEntry():
    hash =  request.form["hash"]
    timestamp = request.form["timestamp"]
    type = request.form["type"]
    author = request.form["type"]

    


