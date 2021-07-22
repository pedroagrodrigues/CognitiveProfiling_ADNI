
import os, sys

path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if path not in sys.path:
    sys.path.append(path)
    os.chdir(path)



import pandas as pd
import numpy as np
import json

def loadFile(name: str) -> pd.DataFrame:
    return pd.read_pickle("Data/local/"+name+".pickle")

def saveFile(data: pd.DataFrame, name: str, csv: bool = False) ->None:
    if csv:
        data.to_csv("Data/local/"+name+".csv")
    else: data.to_pickle("Data/local/"+name+".pickle")