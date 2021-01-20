import numpy as np
import pandas as panda
import json
# Load data from database:
from Database import Database

path = './dataFiles/ADNI_MERGE'

try:
    data = panda.read_pickle(path+'.pickle')
except:
    credentials = json.load(open("credentials.json"))

    db = Database('ADNI', 'ADNIMERGE', credentials['user'], credentials['password'])

    labelsToRemove = ['_id', 'RID', 'PTID', 'SITE', 'COLPROT', 'ORIGPROT', 'PRID', 'EXAMDATE', 'EXAMDATE_bl', 'Years_bl', 'Month_bl', 'Month', 'M']
    # this field is the object id generated from MongoDB, we dont need it.
    labels = [label for label in db.getLabels() if label not in labelsToRemove]

    # Saving into a file just to increase performance while debugging.
    data = panda.DataFrame({label : db.getColumn(label) for label in labels})
    data.to_pickle(path+'.pickle')
    data.to_csv(path+'.csv') #easier to see

#data[targetLabel] = panda.get_dummies(data[targetLabel])
def getUniqueCategories(data):
    for col in data:
        if data[col].dtypes == 'object':
            unique = len(data[col].unique())
            print(f"Feature \033[33m '{col}' \033[0m has \033[33m {unique} \033[0m unique categories")

#### Target data setup:
### Fixing Labels
# Some of the subjects were between diagnosis. 
# Since they seem to be changing between two of 
# them, I've decided to consider the target of 
# this change, example if the diagnosis was MCI to 
# Dementia the model will treat this subject as Dementia.
# The alternative to this was to remove this row or to 
# create a new target like "other" 

# 'MCI to Dementia' -> 'Dementia'  (284)
# 'NL to MCI'       -> 'MCI'       (76)
# 'MCI to NL'       -> 'NL'        (57)
# 'Dementia to MCI' -> 'MCI'       (6)
# 'NL to Dementia'  -> 'Dementia'  (3)

# Also labels must be converted to a numeric value corresponding to their number
# 'NA'       -> 0
# 'MCI'      -> 1
# 'NL'       -> 2
# 'Dementia' -> 3
###
targetLabel = 'DX'

data[targetLabel] = [ 3 if value == 'MCI to Dementia' or value == 'NL to Dementia' or value == 'Dementia' else value for value in data[targetLabel]]
data[targetLabel] = [ 1 if value == 'NL to MCI' or value == 'Dementia to MCI' or value == 'MCI' else value for value in data[targetLabel]]
data[targetLabel] = [ 2 if value == 'MCI to NL' or value == 'NL' else value for value in data[targetLabel]]
data[targetLabel] = [ 0 if value == 'NA' else value for value in data[targetLabel]]

# X is the data, y is the target or value corresponding to this data
x = data.drop(targetLabel, 1)
y = data[targetLabel]

#Same process is applied to DX_bl



print(x['DX_bl'].value_counts())

# for i in x:
#     print (f"Categories for \033[33m '{i}' \033[0m category")
#     print(x[i].value_counts())
#     input('press enter to proceed')

# getUniqueCategories(x)

