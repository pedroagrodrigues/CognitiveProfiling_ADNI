# External imports
import pandas as panda
import json

# Internal imports
from Database import Database


class Moca:
    def __init__(self):
        self.path = './dataFiles/MOCA'
        self.data = self.getData()
        print("Moca ready!")

    def getData(self):
        try:
            data = panda.read_pickle(self.path + '.pickle')
        except:
            credentials = json.load(open("credentials.json"))

            db = Database('ADNI', 'MOCA', credentials['user'], credentials['password'], credentials['server'])

            labelsToRemove = ['_id', 'VISCODE', 'USERDATE', 'USERDATE2', 'update_stamp']

            labels = [label for label in db.getLabels() if label not in labelsToRemove]

            data = panda.DataFrame({label: db.getColumn(label) for label in labels})

            data['Phase'] = [1 if x == 'ADNI1' else x for x in data['Phase']]
            data['Phase'] = [2 if x == 'ADNI2' else x for x in data['Phase']]
            data['Phase'] = [3 if x == 'ADNI3' else x for x in data['Phase']]
            data['Phase'] = [4 if x == 'ADNIGO' else x for x in data['Phase']]

            fieldsToInt = ['ID', 'RID', 'SITEID']

            for field in fieldsToInt:
                data = self.dataToInt(data, field)

            data = data.loc[data['VISCODE2'] != '']
            data['VISCODE2'] = [int(x.lstrip('m').lstrip('0')) if x != 'bl' else 0 for x in data['VISCODE2']]

            fieldsToClean = ['TRAILS', 'CUBE', 'CLOCKCON', 'CLOCKNO', 'CLOCKHAN',
                             'LION', 'RHINO', 'CAMEL', 'IMMT1W1', 'IMMT1W2', 'IMMT1W3', 'IMMT1W4',
                             'IMMT1W5', 'IMMT2W1', 'IMMT2W2', 'IMMT2W3', 'IMMT2W4', 'IMMT2W5', 'DIGFOR',
                             'DIGBACK', 'LETTERS', 'SERIAL1', 'SERIAL2', 'SERIAL3', 'SERIAL4',
                             'SERIAL5', 'REPEAT1', 'REPEAT2', 'FFLUENCY', 'ABSTRAN', 'ABSMEAS',
                             'DELW1', 'DELW2', 'DELW3', 'DELW4', 'DELW5', 'DATE', 'MONTH', 'YEAR', 'DAY',
                             'PLACE', 'CITY', 'MOCA']

            for field in fieldsToClean:
                data = self.dataCleaner(data, field)

            for row in data['ID']:
                data.loc[data['ID'] == row, 'MOCA'] = self.calculateTotals(data.loc[data['ID'] == row])

            data.to_pickle(self.path + '.pickle')
            data.to_csv(self.path + '.csv')

        return data

    def dataCleaner(self, data, field):
        # 1st approach
        data = data.loc[data[field] != '']
        data[field] = [int(x) for x in data[field]]
        # 2nd approach
        # data[field] = [0 if x == '' else int(x) for x in data[field]]

        return data

    def dataToInt(self, data, field):
        data[field] = [int(x) for x in data[field]]
        return data

    def calculateTotals(self, row):
        dataLabels = ['TRAILS', 'CUBE', 'CLOCKCON', 'CLOCKHAN', 'CLOCKNO', 'LION', 'RHINO',
                      'CAMEL', 'DIGFOR', 'DIGBACK', 'REPEAT1', 'REPEAT2', 'ABSTRAN', 'ABSMEAS', 'DATE',
                      'MONTH', 'YEAR', 'DAY', 'PLACE', 'CITY']

        total = 0
        for label in dataLabels:
            total += row[label].values[0]

        temp = 0
        for i in range(1, 6):
            temp += row['SERIAL'+str(i)].values[0]

        if temp > 0:
            total += 1
        if temp > 1:
            total += 1
        if temp > 3:
            total += 1

        for i in range(1, 6):
            if row['DELW'+str(i)].values[0] == 1:
                total += 1

        if row["LETTERS"].values[0] < 2:
            total += 1
        if row["FFLUENCY"].values[0] > 10:
            total += 1

        return round(total * 100 / 30, 2)


x = Moca()

print(x.data.head(5))
