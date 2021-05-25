if __name__ == "__main__":
    from common import *
else: 
    from .common import *

class Ecogsp:
    def __init__(self) -> None:
        self.name = "ECOGSP"
        self.data = self.prepareData()

    def prepareData(self) -> pd.DataFrame:
        try:
            return loadFile(self.name)
        except:
            labels = getLabels(self.name)
            labelsToRemove = ["_id", "index", "PHASE", "ID", "SITEID", "USERDATE", "USERDATE2", "SPID", "update_stamp"]
            labels = [label for label in labels if label not in labelsToRemove]
            data = loadData(self.name, labels)
            saveFile(data, self.name)
            return data
