
if __name__ == "__main__":
    from common import *
else:
    from .common import *



class Cdr:
    def __init__(self):
        self.name = 'CDR'
        self.dataLoader()
        print("CDR ready!")

    def dataLoader(self):
        try:
            self.data = loadFile(self.name)
        except:
            labels = getLabels(self.name)
            labelsToRemove = ['_id', 'Phase', 'VISCODE', 'USERDATE', 'USERDATE2', 'EXAMDATE', 'CDVERSION', 'CDSOB', 'update_stamp']
            labels = [label for label in labels if label not in labelsToRemove]
            data = loadData(self.name, labels)
            self.fixCodes(data)
            self.dataToNumeric(data)
            self.calculateTotals(data)
            saveFile(self.data, self.name)

    def fixCodes(self, data: pd.DataFrame) -> None:
        data.rename(columns={"VISCODE2": "VISCODE"}, inplace=True)
        data["VISCODE"].replace({"sc": "bl"}, inplace=True)

    def dataToNumeric(self, data: pd.DataFrame) -> None:
        fields = ['ID', 'RID', 'SITEID', 'CDSOURCE', 'CDMEMORY', 'CDORIENT', 'CDJUDGE', 'CDCOMMUN', 'CDHOME', 'CDCARE', 'CDGLOBAL']
        for field in fields:
            data[field] = pd.to_numeric(data[field])

    def calculateTotals(self, data: pd.DataFrame) -> None:
        fields = ['CDMEMORY', 'CDORIENT', 'CDJUDGE', 'CDCOMMUN', 'CDHOME', 'CDCARE']
        data["CDRSB"] = data[fields].sum(axis=1)
        self.data = data.dropna()

