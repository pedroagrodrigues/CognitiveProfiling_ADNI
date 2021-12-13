if __name__ == "__main__":
    from common import *
else:
    from .common import *

class Faq:
    def __init__(self) -> None:
        self.name = "FAQ"
        self.dataLoader()

    def dataLoader(self) -> None:
        try:
            self.data = loadFile(self.name)
        except:
            labelsToRemove = ['_id', 'index', 'ID', 'VISCODE', 'USERDATE', 'EXAMDATE', 'USERDATE2', 'SPID', 'update_stamp']
            labels = [label for label in getLabels(self.name) if label not in labelsToRemove]
            data = loadData(self.name, labels)
            data.rename(columns={"VISCODE2": "VISCODE"}, inplace=True)
            data["RID"] = pd.to_numeric(data["RID"])
            saveFile(data, self.name)
            self.data = data
