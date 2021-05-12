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

    

    def query(self, target, dataFilter=None):
        """[summary]
        Args:
            target (Dict, String): if Dict -> {Field: Value, Field: Value...} if String -> Column name
            dataFilter (String, optional): Filters distinct values of dataFilter. Defaults to None.

        """
        print(target)
        if type(target) == dict:
            if dataFilter != None:
                try: 
                    return self.dbConnect().find(target).distinct(dataFilter)
                except Exception(e):
                    print("Something wrong with your query: ", e)
            return self.dbConnect().find(target)
        try:
            return self.dbConnect().find(target[0], target[1])
        except:
            print("There is an error in your query: Target type not dict.")