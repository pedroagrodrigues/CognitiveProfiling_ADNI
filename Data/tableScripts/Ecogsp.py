if __name__ == "__main__":
    from common import *
else: 
    from .common import *

class Ecogsp:
    def __init__(self) -> None:
        self.name = "ECOGSP"
        self.dataLoader()

    def dataLoader(self) -> None:
        try:
            self.data = loadFile(self.name)
        except:
            labels = getLabels(self.name)
            labelsToRemove = ["_id", "index", "VISCODE", "PHASE", "ID", "SITEID", "USERDATE", "USERDATE2", "SPID", "update_stamp"]
            labels = [label for label in labels if label not in labelsToRemove]
            data = loadData(self.name, labels)
            self.fixCodes(data)
            self.data = data.dropna()


    def fixCodes(self, data: pd.DataFrame) -> None:
        data.rename(columns={ "VISCODE2" : "VISCODE" }, inplace=True)
    
    def calculateTotals(self, data: pd.DataFrame) -> None:
        pass
        
