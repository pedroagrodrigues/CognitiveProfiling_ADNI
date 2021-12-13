if __name__ == "__main__":
    from common import *
else:
    from .common import *


class Ecogpt:
    def __init__(self) -> None:
        self.name = "ECOGPT"
        self.dataLoader()

    def dataLoader(self) -> None:
        try:
            self.data = loadFile(self.name)
        except:
            labelsToRemove = ['_id', 'index', 'Phase', 'ID',
                              'SITEID', 'VISCODE', 'USERDATE', 'USERDATE2', 'update_stamp']
            labels = [label for label in getLabels(self.name) if label not in labelsToRemove]
            data = loadData(self.name, labels)
            data['RID'] = pd.to_numeric(data['RID'])
            data.rename(columns={"VISCODE2": "VISCODE"}, inplace=True)
            self.renameCols(data)
            saveFile(data, self.name)
            self.data = data

    def renameCols(self, data: pd.DataFrame) -> None:
        fields = ['MEMORY1', 'MEMORY2', 'MEMORY3', 'MEMORY4', 'MEMORY5', 'MEMORY6',
                  'MEMORY7', 'MEMORY8', 'LANG1', 'LANG2', 'LANG3', 'LANG4', 'LANG5',
                  'LANG6', 'LANG7', 'LANG8', 'LANG9', 'VISSPAT1', 'VISSPAT2', 'VISSPAT3',
                  'VISSPAT4', 'VISSPAT5', 'VISSPAT6', 'VISSPAT7', 'VISSPAT8', 'PLAN1',
                  'PLAN2', 'PLAN3', 'PLAN4', 'PLAN5', 'ORGAN1', 'ORGAN2', 'ORGAN3',
                  'ORGAN4', 'ORGAN5', 'ORGAN6', 'DIVATT1', 'DIVATT2', 'DIVATT3',
                  'DIVATT4', 'SOURCE']

        for field in fields:
            temp = field+'_PT'
            data.rename(columns={ field : temp}, inplace=True)