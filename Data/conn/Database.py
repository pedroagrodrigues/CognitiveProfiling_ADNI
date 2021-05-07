from pymongo import MongoClient

class Database:
    def __init__(self, database, collection, username, password, path='localhost', port=27017):
        self.database = database
        self.collection = collection
        self.path = path
        self.port = port
        self.username = username
        self.password = password

    def dbConnect(self):
        try:
            return MongoClient(self.path, self.port, username=self.username, password=self.password)[self.database][self.collection]
        except: 
            raise Exception("Something went wrong. check path, port and access permitions. Is the name of your collection right?")

    def getLabels(self):
        collection = self.dbConnect()
        return [label for label in collection.find_one()] 

    def getUnlabelledData(self):
        try:
            return [list(row.values()) for row in self.dbConnect().find({})]
        except Exception as error:
            print("Something went wrong: " + repr(error))

    def getData(self):
        try:
            return self.dbConnect().find({})
        except Exception as error:
            print("Something went wrong: " + repr(error))

    def getColumn(self, column):
        try: 
            return [row[column] for row in self.dbConnect().find({}, {column:1})]
        except Exception as error:
            print("Something went wrong: " + repr(error))

    

    def query(self, target, dataFilter=None, distinct=True):
        if distinct:
            if type(target) != dict and dataFilter is None:
                return self.dbConnect().distinct(target)
            return self.dbConnect().distinct(target, dataFilter)
        return self.dbConnect().find(target, dataFilter)



