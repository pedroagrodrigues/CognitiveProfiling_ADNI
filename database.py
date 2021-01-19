from pymongo import MongoClient
import json

credentials = json.load(open("credentials.json"))
collectionName = "ADNI"
tableName="ADNI_TQ1"

def dbConnect(collection=collectionName, table=tableName, path='localhost', port=27017, loginData=credentials):
    if 'user' not in loginData or 'password' not in loginData: 
        raise Exception("Error: logindata must contain user and password")
    try:
        return MongoClient(path, port, username=loginData['user'], password=loginData['password'])[collection][table]
    except: 
        raise Exception("Something went wrong. check path, port and access permitions.")

def getLabels():
    collection = dbConnect()
    return [label for label in collection.find_one()] 

def getUnlabledData():
    collection = dbConnect()
    try:
        return [list(row.values()) for row in collection.find({})]
    except Exception as error:
        print("Something went wrong: " + repr(error))

def getData():
    try:
        return dbConnect().find({})
    except Exception as error:
        print("Something went wrong: " + repr(error))

def getColumn(column):
    try: 
        return [row[column] for row in dbConnect().find({}, {column:1})]
    except Exception as error:
        print("Something went wrong: " + repr(error))





