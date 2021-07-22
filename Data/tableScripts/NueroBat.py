from numpy import save


if __name__ == "__main__":
    from common import *
else: 
    from .common import *

class Neurobat:
    def __init__(self) -> None:
        self.name = "NEUROBAT"
        self.dataLoader()
        # print(self.data.head())
    
    def dataLoader(self) -> None:
        try:
            self.data = loadFile(self.name)
        except:
            labelsToRemove = ['_id', 'index', 'Phase', 'ID', 'SITEID', 'VISCODE2', 'USERDATE', 'USERDATE2', 'EXAMDATE', 'update_stamp']
            labels = [label for label in getLabels(self.name) if label not in labelsToRemove]
            data = loadData(self.name, labels)
            # self.fixCodes(data)
            data["RID"] = pd.to_numeric(data["RID"])
            saveFile(data, self.name)
            self.data = data
    
    def fixCodes(self, data:pd.DataFrame) -> None:
        data["VISCODE"].replace({"sc": "bl"}, inplace=True)
        data["VISCODE"].replace({"v01": "bl"}, inplace=True)
        data["VISCODE"].replace({"v11": "m12"}, inplace=True)
        data["VISCODE"].replace({"y4": "m108"}, inplace=True)
        print(data['VISCODE'].value_counts())



