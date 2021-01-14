import numpy as np

from database import getLabels, getColumn

labels = getLabels()
target = 'DX'

# labelToRemove = ['_id', 'RID', 'PTID', 'SITE', 'DX']



content = {}

# print(labels)

for label in labels:
    data = getColumn(label)
    content[label] = data




print(content['DX'])
        
# for i in content:
    # print(i)