
import pandas as panda

import json

import common


from Data import Database

import Mmse
import Moca
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
mergeData = panda.DataFrame(db["ADNIMERGE"].query([{"MOCA": {"$ne": ""}, "MMSE": {
                            "$ne": ""}, "VISCODE": "bl"}, {"RID": 1, "MOCA": 1, "MMSE": 1, "_id": 0}]))

# At the moment we have all Roaster IDs (1433) from the table ADNIMERGE with both MMSE and MOCA filled also filtering just the baselines.

# Now download the RID and Total for MMSE and MOCA
mmseData = Mmse()
mocaData = Moca()


# print(len(mmseData.loc[mmseData['RID'] == "6000008"]))

# mocaData = panda.DataFrame(db["MOCA"].query([{"MOCA": "6008", "VISCODE": "bl"}, {"RID" : 1, "MOCA" : 1, "_id" : 0}]))
# print(mocaData)


# Next step is to compare these totals with the ones from merge table
# totalValid = 0
# moca = mmse = 0
# for index, row in mergeData.iterrows():
#     valid = True
#     if len(mmseData.loc[mmseData['RID'] == row['RID']]) == 1:
#         mmse += 1
#     else: valid = False

#         # mmse = mmseData.loc[mmseData['RID'] == row["RID"]]["MMSCORE"].iloc[0]
#     if len(mocaData.loc[mocaData['RID'] == row['RID']]) == 1:
#         moca += 1
#     else: valid = False
#         # moca = mocaData.loc[mocaData['RID'] == row["RID"]]["MOCA"].iloc[0]

#     if valid:
#         totalValid += 1

# print("Total merged with current filter: ", len(mergeData))
# print("Total of maches found: ", totalValid, " Moca: ", moca, " MMSE: ", mmse)
# print("Total lines from Moca: ", len(mocaData))
# print("Total lines from MMSE: ", len(mmseData))
