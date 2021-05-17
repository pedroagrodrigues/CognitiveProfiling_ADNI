import pandas as panda
import json

from . import common
from Data import Database


class Mmse:
    def __init__(self):
        self.path = 'Data/local/MMSE'
        self.data = self.getData()
        print("MMSE ready!")

    def getData(self):
        try:
            data = panda.read_pickle(self.path + '.pickle')
        except:
            credentials = json.load(open("config/credentials.json"))

            db = Database('ADNI', 'MMSE', credentials['user'], credentials['password'], credentials['server'])

            # labelsToRemove = ['_id']
            labelsToRemove = ['_id', 'USERDATE', 'USERDATE2', 'update_stamp', 'EXAMDATE', 'MMDATECM',
                              'MMYEARCM', 'MMMNTHCM', 'MMDAYCM', 'MMSESNCM', 'MMRECALL', 'MMTRIALS', 'MMHOSPCM', 'MMFLRCM',
                              'MMCITYCM', 'MMAREACM', 'MMSTCM', 'MMTRIALS', 'MMDLTR', 'MMLLTR', 'MMRLTR',
                              'MMOLTR', 'MMWLTR', 'MMLTR1', 'MMLTR2', 'MMLTR3', 'MMLTR4', 'MMLTR5',
                              'MMLTR6', 'MMLTR7', 'DONE', 'MMLTR1', 'MMLTR2', 'MMLTR3', 'MMLTR4', 'MMLTR5',
                              'MMLTR6', 'MMLTR7', 'WORD1', 'WORD1DL', 'WORD2', 'WORD2DL', 'WORD3', 'WORD3DL',
                              'WORDLIST', 'WORLDSCORE', 'update_stamp']

            labels = [label for label in db.getLabels() if label not in labelsToRemove]

            data = panda.DataFrame({label: db.getColumn(label) for label in labels})


            data['Phase'] = [1 if x == 'ADNI1' else x for x in data['Phase']]
            data['Phase'] = [2 if x == 'ADNI2' else x for x in data['Phase']]
            data['Phase'] = [3 if x == 'ADNI3' else x for x in data['Phase']]
            data['Phase'] = [4 if x == 'ADNIGO' else x for x in data['Phase']]

            fieldsToInt = ['ID', 'RID', 'SITEID']
            for field in fieldsToInt:
                data = self.dataToInt(data, field)

            fieldsToClean = ['MMDATE', 'MMYEAR',
                             'MMMONTH', 'MMDAY', 'MMSEASON', 'MMHOSPIT', 'MMFLOOR', 'MMCITY',
                             'MMAREA', 'MMSTATE', 'MMBALL', 'MMFLAG', 'MMTREE', 'MMBALLDL',
                             'MMFLAGDL', 'MMTREEDL', 'MMWATCH', 'MMPENCIL', 'MMREPEAT', 'MMHAND',
                             'MMFOLD', 'MMONFLR', 'MMREAD', 'MMWRITE', 'MMDRAW', 'MMD', 'MML', 'MMR',
                             'MMO', 'MMW']

            for field in fieldsToClean:
                data = self.dataClean(data, field)

            for row in data['ID']:
                data.loc[data['ID'] == row, 'MMSCORE'] = self.calculateTotals(data.loc[data['ID'] == row], fieldsToClean)

            data.to_pickle(self.path + '.pickle')

        return data

    def dataToInt(self, data, field):
        data = data.loc[(data[field] != '-1') & (data[field] != '')]
        data[field] = [int(x) for x in data[field]]

        return data

    def dataClean(self, data, field):
        data = data.loc[(data[field] != '-1') & (data[field] != '')]
        data[field] = [1 if x == '1' else 0 for x in data[field]]

        return data

    def calculateTotals(self, row, fields):
        return sum(row[i].values[0] for i in fields)
        # return round(total * 100 / 30, 2)

# Debug:
# x = Mmse()
# print(x.data.head(5))
# data['MMSCORE'] = [calcTotal(row, fieldsToClean) for row in data.loc]
# print(data.dtypes)

# print(data.head(10))
# print(data.loc[(data['ID'] == 44) & (data['RID'] == 25)]['MMSCORE'])
# print(calcTotal(data.loc[(data['ID'] == 44) & (data['RID'] == 25)], fieldsToClean))
# print(data['SITEID'].value_counts)
