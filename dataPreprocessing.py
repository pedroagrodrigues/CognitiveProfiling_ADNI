import numpy as np
import pandas as panda
from sklearn.preprocessing import scale
from statsmodels.nonparametric.kde import KDEUnivariate

import json
# Load data from database:
from Database import Database


def findOutliersTukey(data):
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1 
    floor = q1 - 1.5 * iqr
    ceiling = q3 + 1.5 * iqr
    outlierIndices = [data.index(x) for x in data if x < floor or x > ceiling]
    outlierValues = [data[x] for x in outlierIndices]
    return outlierIndices, outlierValues

def findOutliersKDE(data):
    data_scaled = scale(list(map(float,data)))
    kde = KDEUnivariate(data_scaled)
    kde.fit(bw="scott", fft=True)
    pred = kde.evaluate(data_scaled)

    n = sum(pred < 0.05)
    outlierIndices = np.array(pred).argsort()[:n]
    outlierValues = np.array(data)[outlierIndices]
    return outlierIndices, outlierValues
    



path = './dataFiles/TQ1'

try:
    data = panda.read_pickle(path + '.pickle')
except:
    credentials = json.load(open("credentials.json"))

    db = Database('ADNI', 'ADNI_TQ1', credentials['user'], credentials['password'])

    labelsToRemove = ['_id', 'RID', 'PTID', 'EXAMDATE']
    # this field is the object id generated from MongoDB, we dont need it.
    labels = [label for label in db.getLabels() if label not in labelsToRemove]

    # Saving into a file just to increase performance while debugging.
    data = panda.DataFrame({label : db.getColumn(label) for label in labels})
    data.to_pickle(path + '.pickle')
    data.to_csv(path + '.csv')


data['DX_bl'] = [0 if value == 'CN' else value for value in data['DX_bl']]
data['DX_bl'] = [1 if value == 'LMCI' else value for value in data['DX_bl']]
data['DX_bl'] = [2 if value == 'EMCI' else value for value in data['DX_bl']]
data['DX_bl'] = [3 if value == 'AD' else value for value in data['DX_bl']]

data['VISCODE'] = [0 if value == 'bl' else 1 for value in data['VISCODE']]
data['AGE'] = [eval(age) for age in data['AGE']]
data['PTGENDER'] = [1 if x == 'Male' else 0 for x in data['PTGENDER']]
data['APOE4'] = [eval(x) for x in data['APOE4']]
data['MMSE'] = [eval(x) for x in data['MMSE']]
data['APOE_Genotype'] = [eval(x) for x in [y.replace(',','.') for y in data['APOE_Genotype']]]

print(data.head(5))


# There are outliers in the data but ignored for the time being
# print(findOutliersTukey([x for x in data["AGE"]]))
# print(findOutliersKDE([x for x in data["AGE"]]))

