
if __name__ == "__main__":
    from common import *
else:
    from .common import *

class Moca:
    def __init__(self):
        self.name = "MOCA"
        self.dataLoader()
        print("Moca ready!")

    def dataLoader(self):
        try:
            self.data = loadFile(self.name)
        except:
            labels = getLabels(self.name)
            labelsToRemove = ['_id', 'Phase', "VISCODE", 'USERDATE', 'USERDATE2', 'update_stamp']
            labels = [label for label in labels if label not in labelsToRemove]
            data = loadData(self.name, labels)
            data.rename(columns={ "VISCODE2" : "VISCODE" }, inplace=True)
            self.dataToInt(data)
            self.calculateTotals(data)
            saveFile(self.data, self.name)

    def dataToInt(self, data: pd.DataFrame) -> None:
        fields = ['TRAILS', 'CUBE', 'CLOCKCON', 'CLOCKNO', 'CLOCKHAN',
                'LION', 'RHINO', 'CAMEL', 'IMMT1W1', 'IMMT1W2', 'IMMT1W3', 'IMMT1W4',
                'IMMT1W5', 'IMMT2W1', 'IMMT2W2', 'IMMT2W3', 'IMMT2W4', 'IMMT2W5', 'DIGFOR',
                'DIGBACK', 'LETTERS', 'SERIAL1', 'SERIAL2', 'SERIAL3', 'SERIAL4',
                'SERIAL5', 'REPEAT1', 'REPEAT2', 'FFLUENCY', 'ABSTRAN', 'ABSMEAS',
                'DELW1', 'DELW2', 'DELW3', 'DELW4', 'DELW5', 'DATE', 'MONTH', 'YEAR', 'DAY',
                'PLACE', 'CITY', 'MOCA']
        for field in fields:
            data[field] = pd.to_numeric(data[field])
        
        


    def calculateTotals(self, data: pd.DataFrame) -> None:
        validFields = ['TRAILS', 'CUBE', 'CLOCKCON', 'CLOCKHAN', 'CLOCKNO', 'LION', 'RHINO',
                      'CAMEL', 'DIGFOR', 'DIGBACK', 'REPEAT1', 'REPEAT2', 'ABSTRAN', 'ABSMEAS', 'DATE',
                      'MONTH', 'YEAR', 'DAY', 'PLACE', 'CITY']
        data["MOCA"] = data[validFields].sum(axis=1)

        for index, row in data.iterrows():
            temp = sum(row['SERIAL'+str(i)] for i in range(1, 6))

            specialFieldsTotal = 0
            if temp > 0: 
                specialFieldsTotal += 1
            if temp > 1:
                specialFieldsTotal += 1
            if temp > 3:
                specialFieldsTotal += 1
            for i in range(1,6):   
                if row['DELW'+str(i)] == 1:
                    specialFieldsTotal += 1
            if row["LETTERS"] < 2:
                specialFieldsTotal += 1
            if row["FFLUENCY"] > 10:
                specialFieldsTotal += 1
            data.loc[index, "MOCA"] += specialFieldsTotal
            
        self.data = data.dropna()


