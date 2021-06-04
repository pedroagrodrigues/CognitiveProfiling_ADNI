from numpy import save


if __name__ == "__main__":
    from common import *
else: 
    from .common import *

class Neurobat:
    def __init__(self) -> None:
        self.name = "NEUROBAT"
        self.dataLoader()
    
    def dataLoader(self) -> None:
        try:
            self.data = loadFile(self.name)
        except:
            labelsToRemove = ['_id', 'index', 'Phase', 'ID', 'SITEID', 'VISCODE', 'USERDATE', 'USERDATE2', 'EXAMDATE', 'update_stamp']
            labels = [label for label in getLabels(self.name) if label not in labelsToRemove]
            data = loadData(self.name, labels)
            data.rename(columns={ "VISCODE2" : "VISCODE"}, inplace=True)
            data["RID"] = pd.to_numeric(data["RID"])
            saveFile(data, self.name)
            self.data = data
        