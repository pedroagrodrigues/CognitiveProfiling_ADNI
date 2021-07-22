
if __name__ == "__main__":
    from common import *
else:
    from .common import *

class Moca:
    def __init__(self):
        self.name = "MOCA"
        self.dataLoader()

    def dataLoader(self):
        try:
            self.data = loadFile(self.name)
        except:
            labels = getLabels(self.name)
            labelsToRemove = ['_id', 'ID', 'SITEID', 'Phase', "VISCODE", 'USERDATE', 'USERDATE2', 'update_stamp']
            labels = [label for label in labels if label not in labelsToRemove]
            data = loadData(self.name, labels)
            data = self.fixCodes(data)
            self.dataToInt(data)
            self.calculateTotals(data)
            saveFile(data, self.name)

    

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
        educ = self.getEduc()
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

            "This is only to check the patient age, sometimes we don't have this information and the try and catch is a workarround. There's a space for improvement using the file Neurobat.py"
            try:
                if int(educ.loc[(educ["RID"] == row['RID']) & (educ["VISCODE"] == row["VISCODE"])]["PTEDUCAT"]) < 13:
                    specialFieldsTotal += 1
            except:
                continue

            data.loc[index, "MOCA"] += specialFieldsTotal

        data["RID"] = pd.to_numeric(data["RID"])
        self.data = data.dropna()

    def getEduc(self) -> pd.DataFrame:
        labels = ['RID', 'VISCODE', 'PTEDUCAT']
        return loadData("ADNIMERGE", labels)

    def fixCodes(self, data: pd.DataFrame) -> pd.DataFrame:
        data.rename(columns={ "VISCODE2" : "VISCODE" }, inplace=True)
        data = data.drop(data[data.VISCODE == ''].index)
        data = data.drop_duplicates(subset=["RID", "VISCODE"], keep=False)
        # # Some columns have a wierd behaviour. 
        # codes = ['bl', 'm06', 'm12', 'm24', 'm36', 'm48', 'm60', 'm72', 'm84', 'm96', 'm108', 'm120', 'm132', 'm144', 'm156', 'm168', 'm180']
        # tooBig = [codes[i] for i in range(1, len(codes[1:])) if len(data.loc[data["VISCODE"] == codes[i]]) > len(data.loc[data["VISCODE"] == codes[i - 1]])]
        return data

