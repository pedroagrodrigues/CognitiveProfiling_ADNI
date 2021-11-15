import os
import sys


path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if path not in sys.path:
    sys.path.append(path)

import pandas as pd
import numpy as np
import json
from Data import Database


def connDatabase(name: str) -> Database:
    """Instantiates the Database class

    Args:
        name (str): "Name of the table you wish to connect"

    Returns:
        Database: Returns a file with the database

    Comments: 
        credentials must be a json file containing at least these variables:
        "user": "user",
        password": "password",
        "server": "mongodb+srv://cluster0.cott4.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        
        This is just an example.
    """
    credentials = json.load(open("config/credentials.json"))
    return Database('ADNI', name, credentials['user'], credentials['password'], credentials['server'])


def loadFile(name: str) -> pd.DataFrame:
    """Loads a file locally

    Args:
        name (str): Name of the file you wish to load

    Returns:
        pd.DataFrame: Data from the file
    """
    return pd.read_pickle("Data/local/"+name+".pickle")

def saveFile(data: pd.DataFrame, name: str, csv: bool = False) ->None:
    """Saves the file locally

    Args:
        data (pd.DataFrame): Data for the file
        name (str): Name of the file
        csv (bool, optional): If true, saves the file as CSV for better visualisation. Defaults to False.
    """
    if csv:
        data.to_csv("Data/local/"+name+".csv")
    else: data.to_pickle("Data/local/"+name+".pickle")

def loadData(name: str, labels: list) -> pd.DataFrame:
    """Loads the file from the database

    Args:
        name (str): Name of the data table
        labels (list): Fields to load

    Returns:
        pd.DataFrame: Data loaded
    """
    db = connDatabase(name)
    return pd.DataFrame({label : db.getColumn(label) for label in labels})

def getLabels(name: str) -> list:
    """Get labels from database

    Args:
        name (str): Table name

    Returns:
        list: list of labels
    """
    db = connDatabase(name)
    return [label for label in db.getLabels()]

def insertFileDB(data: pd.DataFrame, name: str) -> None:
    """Saves a new table to the database

    Args:
        data (pd.DataFrame): Table to load in database
        name (str): Name of the new table
    """
    connDatabase(name).insertMany(data)
    