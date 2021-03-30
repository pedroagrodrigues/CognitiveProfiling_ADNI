from Merge import Merge
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Warning, ignoring some errors that will result in a NaN value of the output matrix


path = './dataFiles/corr'


def getCorr(x, y):
    xData = []
    yData = []
    for i in range(len(x)):
        if x[i] != '' and y[i] != '':
            xData.append(eval(str(x[i])))
            yData.append(eval(str(y[i])))

    xData = np.array(xData)
    yData = np.array(yData)
    return np.corrcoef(xData, yData)[0, 1]


try:
    correlations = pd.read_pickle(path+'.pickle')
except:
    data = Merge().data

    unusedLables = ['RID', 'PTID', 'VISCODE', 'SITE', 'COLPROT', 'ORIGPROT']

    data = data.drop(columns=unusedLables)

    dataLabels = data.columns.values
    dataNumpy = data.to_numpy()

    correlations = pd.DataFrame(index=dataLabels, columns=dataLabels)

    for i in range(len(dataLabels)):
        correlations.at[dataLabels[i], dataLabels[i]] = 1
        for j in range(i+1, len(dataLabels)):
            corr = getCorr(dataNumpy[:, i], dataNumpy[:, j])
            correlations.at[dataLabels[i], dataLabels[j]] = correlations.at[dataLabels[j], dataLabels[i]] = 0 if np.isnan(corr) else abs(corr)

    correlations.to_pickle(path+'.pickle')
    correlations.to_csv(path+'.csv')

# correlations.fillna(0)
# print(correlations.head(10))

# sns.set_theme()
# plt.pcolor(correlations)
# plt.yticks(np.arange(0.5, len(correlations.index), 1), correlations.index)
# plt.xticks(np.arange(0.5, len(correlations.columns), 1), correlations.columns)
# plt.show()


# sns.heatmap(np.ma.filled(correlations.astype(float), np.nan), annot=True, annot_kws={"size": 7}, xticklabels=correlations.columns, yticklabels=correlations.index)

# plt.show()

# print(correlations.head(10))
# print(data.head(5))
