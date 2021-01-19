import numpy as np
import pandas as panda

# Load data from database:
from database import getLabels, getColumn


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


# Target setup
targetLabel = 'DX'

# Some of the labels are inbetween values, since they are too 
# few and may disturb the mode, I've consider them to be the transition target. 
# Alternative was to remove these rows. 
# # These values are changed as it follows:
# 'MCI to Dementia' -> 'Dementia'  (284)
# 'NL to MCI'       -> 'MCI'       (76)
# 'MCI to NL'       -> 'NL'        (57)
# 'Dementia to MCI' -> 'MCI'       (6)
# 'NL to Dementia'  -> 'Dementia'  (3)

# X['native_country'] = ['United-States ' if x == 'United-States' else 'Other' for x in X['native_country']]

data[targetLabel] = ['Dementia' if value == 'MCI to Dementia' or value == 'NL to Dementia' else value for value in data[targetLabel]]
data[targetLabel] = ['MCI' if value == 'NL to MCI' or value == 'Dementia to MCI' else value for value in data[targetLabel]]
data[targetLabel] = ['NL' if value == 'MCI to NL' else value for value in data[targetLabel]]

x = data.drop(targetLabel, 1)
y = data[targetLabel]

print(y.value_counts())

# for i in x:
#     print (f"Categories for \033[33m '{i}' \033[0m category")
#     print(x[i].value_counts())
#     input('press enter to proceed')

# getUniqueCategories(x)

