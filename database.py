from pymongo import MongoClient
import json

credentials = json.load(open("user.json"))
collectionName = "ADNI"
tableName="ADNIMERGE"

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


client = dbConnect()
collection = client.ADNI.ADNIMERGE
    

# print("===============   ADNI 1   ===============")
# print("Subjects of ADNI 1: ", len(collection.distinct("PTID",{"ORIGPROT" : "ADNI1"})))
# print("Subjects in normal controls: ", len(collection.distinct("PTID",{"ORIGPROT" : "ADNI1", "DX_bl": "CN"})))
# print("Subjects with  SMC: ", len(collection.distinct("PTID",{"ORIGPROT" : "ADNI1", "DX_bl": "SMC"})))
# print("Subjects with EMCI: ", len(collection.distinct("PTID",{"ORIGPROT" : "ADNI1", "DX_bl": "EMCI"})))
# print("Subjects with LMCI: ", len(collection.distinct("PTID",{"ORIGPROT" : "ADNI1", "DX_bl": "LMCI"})))
# print("Subjects with AD: ", len(collection.distinct("PTID",{"ORIGPROT" : "ADNI1", "DX_bl": "AD"})), "\n")

# print("===============   ADNI 2   ===============")
# print("Subjects of ADNI 2: ", len(collection.distinct("PTID",{"ORIGPROT" : "ADNI2"})))
# print("Subjects in normal controls: ", len(collection.distinct("PTID",{"ORIGPROT" : "ADNI2", "DX_bl": "CN"})))
# print("Subjects with  SMC: ", len(collection.distinct("PTID",{"ORIGPROT" : "ADNI2", "DX_bl": "SMC"})))
# print("Subjects with EMCI: ", len(collection.distinct("PTID",{"ORIGPROT" : "ADNI2", "DX_bl": "EMCI"})))
# print("Subjects with LMCI: ", len(collection.distinct("PTID",{"ORIGPROT" : "ADNI2", "DX_bl": "LMCI"})))
# print("Subjects with AD: ", len(collection.distinct("PTID",{"ORIGPROT" : "ADNI2", "DX_bl": "AD"})), "\n")



# print("===============   ADNI 3   ===============")
# print("Subjects of ADNI 3: ", len(collection.distinct("PTID",{"ORIGPROT" : "ADNI3"})))
# print("Subjects in normal controls: ", len(collection.distinct("PTID",{"ORIGPROT" : "ADNI3", "DX_bl": "CN"})))
# print("Subjects with  SMC: ", len(collection.distinct("PTID",{"ORIGPROT" : "ADNI3", "DX_bl": "SMC"})))
# print("Subjects with EMCI: ", len(collection.distinct("PTID",{"ORIGPROT" : "ADNI3", "DX_bl": "EMCI"})))
# print("Subjects with LMCI: ", len(collection.distinct("PTID",{"ORIGPROT" : "ADNI3", "DX_bl": "LMCI"})))
# print("Subjects with AD: ", len(collection.distinct("PTID",{"ORIGPROT" : "ADNI3", "DX_bl": "AD"})), "\n")

# print("===============   ADNI GO   ===============")
# print("Subjects of ADNI GO: ", len(collection.distinct("PTID",{"ORIGPROT" : "ADNIGO"})))
# print("Subjects in normal controls: ", len(collection.distinct("PTID",{"ORIGPROT" : "ADNIGO", "DX_bl": "CN"})))
# print("Subjects with MCI: ", len(collection.distinct("PTID",{"ORIGPROT" : "ADNIGO", "DX_bl": "LMCI"})))
# print("Subjects with AD: ", len(collection.distinct("PTID",{"ORIGPROT" : "ADNIGO", "DX_bl": "AD"})), "\n")

    

# print("Subjects of ADNI 1: ", len(collection.distinct("PTID",{"ORIGPROT" : "ADNI1"})))
#     data = collection.distinct("PTID",{"ORIGPROT" : "ADNI1"})
#     data = [eval(x) for x in data]
#     data.sort()
#     print (len(data))
#     # for i in data:
#     #     print(i)
#     #     input()



#     collection = client.ADNI.ADNI1
#     data = collection.distinct("PTID")
#     print(f"ADNI solto: {len(data)}")


        
# except Exception as error:
#     print("Something went wrong: ", error)




