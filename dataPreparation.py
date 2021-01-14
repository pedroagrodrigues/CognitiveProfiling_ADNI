import numpy as np
import pandas as panda

# Load data from database:
from database import getLabels, getColumn

targetLabel = 'DX'

try:
    data = panda.read_pickle('dataset.pickle')
except:
    labelsToRemove = ['_id', 'RID', 'PTID', 'SITE', 'COLPROT', 'ORIGPROT', 'PRID', 'EXAMDATE', 'EXAMDATE_bl', 'Years_bl', 'Month_bl', 'Month', 'M']
    # this field is the object id generated from MongoDB, we dont need it.
    labels = [label for label in getLabels() if label not in labelsToRemove]

    # Saving into a file just to increase performance while debugging.
    data = panda.DataFrame({label : getColumn(label) for label in labels})
    data.to_pickle('dataset.pickle')
    data.to_csv('dataset.csv') #easier to see

#data[targetLabel] = panda.get_dummies(data[targetLabel])
def getUniqueCategories(data):
    for col in data:
        if data[col].dtypes == 'object':
            unique = len(data[col].unique())
            print(f"Feature \033[33m '{col}' \033[0m has \033[33m {unique} \033[0m unique categories")

x = data.drop(targetLabel, 1)
y = data[targetLabel]

for i in x:
    print (f"Categories for \033[33m '{i}' \033[0m category")
    print(x[i].value_counts())
    input('press enter to proceed')

getUniqueCategories(x)

