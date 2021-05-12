import pandas as panda

import json

import common


from Data import Database


credentials = json.load(open("config/credentials.json"))


tables = ['ADNIMERGE', 'MMSE', 'MOCA']





def dictCreator(tableList) -> dict:
    """[summary]

    Args:
        tableList (List): Receives a List containing the name of all the tables required

    Returns:
        dict: Returns a dictionary containing the database object for each table

    """
    return {
        table: Database(
            'ADNI',
            table,
            credentials['user'],
            credentials['password'],
            credentials['server'],
        )
        for table in tableList
    }


db = dictCreator(tables)

# Roaster IDs
rID = db["ADNIMERGE"].query([{"MOCA": {"$ne":""}, "MMSE":{"$ne":""}, "VISCODE": "bl"}, {"RID" : 1, "MOCA" : 1, "MMSE": 1, "_id" : 0}])

mergeData = panda.DataFrame(rID)

print(mergeData.head(10))
print(len(mergeData))

# At the moment we have all Roaster IDs (2288) from the table ADNIMERGE. Now we want to go to each ID and Identify the VISCODE and results for MOCA and MMSE present in ADNIMERGE.

