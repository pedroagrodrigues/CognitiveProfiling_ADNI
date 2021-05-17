import os
import sys


path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if path not in sys.path:
    sys.path.append(path)

import pandas as pd
import json
from Data import Database

def saveToFile(data, name):
    """[Save a File to a given Name]

    Args:
        data (pandas DataFrame): The data to be saved
        name (string): The name of the file to be saved
    """
    path = f"Data/local/{name}.pickle"
    data.to_pickle(path)


def connDatabase(name) -> Database:
    credentials = json.load(open("config/credentials.json"))
    return Database('ADNI', name, credentials['user'], credentials['password'], credentials['server'])


def loadFile(name) -> pd.DataFrame:
    return pd.read_pickle("Data/local/"+name+".pickle")

def saveFile(data, name):
    data.to_pickle("Data/local/"+name+".pickle")

def loadData(name, labels) -> pd.DataFrame:
    db = connDatabase(name)
    return pd.DataFrame({label : db.getColumn(label) for label in labels})

def getLabels(name) -> list:
    db = connDatabase(name)
    return [label for label in db.getLabels()]
