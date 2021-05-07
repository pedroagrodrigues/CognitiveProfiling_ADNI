import pandas as panda
import json

from . import common
from Data import Database



class Cdr:
    def __init__(self):
        self.path = 'data/local/CDR'
        self.data = self.getData()
        print("CDR ready!")

    def getData(self):
        try:
            data = panda.read_pickle(self.path + '.pickle')
        except:
            credentials = json.load(open("config/credentials.json"))

            db = Database('ADNI', 'CDR', credentials['user'], credentials['password'], credentials['server'])

            labelsToRemove = ['_id', 'USERDATE', 'USERDATE2', 'EXAMDATE', 'CDVERSION', 'CDSOB', 'update_stamp']

            labels = [label for label in db.getLabels() if label not in labelsToRemove]

            data = panda.DataFrame({label: db.getColumn(label) for label in labels})

            data['Phase'] = [1 if x == 'ADNI1' else x for x in data['Phase']]
            data['Phase'] = [2 if x == 'ADNI2' else x for x in data['Phase']]
            data['Phase'] = [3 if x == 'ADNI3' else x for x in data['Phase']]
            data['Phase'] = [4 if x == 'ADNIGO' else x for x in data['Phase']]

            fieldsToInt = ['ID', 'RID', 'SITEID', 'CDSOURCE']

            for field in fieldsToInt:
                data = self.dataToInt(data, field)

            fieldsToEvaluate = ['CDMEMORY', 'CDORIENT', 'CDJUDGE', 'CDCOMMUN', 'CDHOME', 'CDCARE', 'CDGLOBAL']

            for field in fieldsToEvaluate:
                data = self.evaluateField(data, field)

            for row in data['ID']:
                data.loc[data['ID'] == row, 'CDRSB'] = self.calculateTotals(data.loc[data['ID'] == row])

            data.to_pickle(self.path + '.pickle')

        return data

    def dataToInt(self, data, field):
        data = data.loc[(data[field] != '-1') & (data[field] != '')]
        data[field] = [int(x) for x in data[field]]

        return data

    def calculateTotals(self, data):
        fields = ['CDMEMORY', 'CDORIENT', 'CDJUDGE', 'CDCOMMUN', 'CDHOME', 'CDCARE']
        return sum(data[field].values[0] for field in fields)

    def evaluateField(self, data, field):
        data = data.loc[(data[field] != '-1') & (data[field] != '')]
        data[field] = [eval(x) for x in data[field]]

        return data


# x = Cdr()

# print(x.data.head(5))
# print (data.loc[data['ID'] == 127785])
# print ('ID: ', eval(data.loc[data['ID'] == 127785, 'CDRSB'].values[0]) == calculateTotals(data.loc[data['ID'] == 127785]))
