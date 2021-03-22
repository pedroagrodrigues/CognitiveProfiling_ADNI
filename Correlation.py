import pandas as pd
import numpy as np
from Merge import Merge

data = Merge().data


def getCorr(x, y):
    xData = []
    yData = []
    for i in range(len(x)):
        if x[i] != '' and y[i] != '':
            xData.append(float(x[i]))
            yData.append(float(y[i]))

    xData = np.array(xData)
    yData = np.array(yData)

    return np.corrcoef(xData, yData)[0, 1]


unusedLables = ['RID', 'PTID', 'VISCODE', 'SITE', 'COLPROT', 'ORIGPROT']

data = data.drop(columns=unusedLables)


dataLabels = data.columns.values
dataNumpy = data.to_numpy()


# index = 17
# print(f"Showing data for {dataLabels[index]}:\n")
# print(dataNumpy[:, index])
correlations = pd.DataFrame(index=dataLabels, columns=dataLabels)

for i in range(len(dataLabels)):
    correlations.at[dataLabels[i], dataLabels[i]] = 1
    for j in range(i+1, len(dataLabels)):
        correlations.at[dataLabels[i], dataLabels[j]] = correlations.at[dataLabels[j], dataLabels[i]] = getCorr(dataNumpy[:, i], dataNumpy[:, j])

print(correlations.head(10))
# print(data.head(5))
