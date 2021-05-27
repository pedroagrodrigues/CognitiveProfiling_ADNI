
if __name__ == "__main__":
    from common import *
else:
    from .common import *

class Mmse:
    def __init__(self) -> None:
        self.name = "MMSE"
        self.path = 'Data/local/MMSE'
        self.dataLoader()
        print("MMSE ready!")

    def dataLoader(self) -> None:
        try:
            self.data = loadFile(self.name)
        except:

            labels = getLabels(self.name)
            labelsToRemove = ['_id', 'VISCODE', 'USERDATE', 'USERDATE2', 'update_stamp', 'EXAMDATE', 'MMDATECM',
                              'MMYEARCM', 'MMMNTHCM', 'MMDAYCM', 'MMSESNCM', 'MMRECALL', 'MMTRIALS', 'MMHOSPCM', 'MMFLRCM',
                              'MMCITYCM', 'MMAREACM', 'MMSTCM', 'MMTRIALS', 'MMDLTR', 'MMLLTR', 'MMRLTR',
                              'MMOLTR', 'MMWLTR', 'MMLTR1', 'MMLTR2', 'MMLTR3', 'MMLTR4', 'MMLTR5',
                              'MMLTR6', 'MMLTR7', 'DONE', 'MMLTR1', 'MMLTR2', 'MMLTR3', 'MMLTR4', 'MMLTR5',
                              'MMLTR6', 'MMLTR7', 'WORD1', 'WORD1DL', 'WORD2', 'WORD2DL', 'WORD3', 'WORD3DL',
                              'WORDLIST', 'WORLDSCORE', 'update_stamp']

            labels = [label for label in labels if label not in labelsToRemove]

            data = loadData(self.name, labels)
            self.fixCodes(data)
            self.calculateTotals(data)

            saveFile(self.data, self.name)

    def fixCodes(self, data: pd.DataFrame) -> None:
        data.rename(columns={"VISCODE2": "VISCODE"}, inplace=True)
        data["VISCODE"].replace({"sc": "bl"}, inplace=True)

    def calculateTotals(self, data: pd.DataFrame) -> None:
        validFields = ['MMDATE', 'MMYEAR', 'MMMONTH', 'MMDAY', 'MMSEASON', 'MMHOSPIT', 'MMFLOOR',
                       'MMCITY', 'MMAREA', 'MMSTATE', 'MMBALL', 'MMFLAG', 'MMTREE', 'MMBALLDL',
                       'MMFLAGDL', 'MMTREEDL', 'MMWATCH', 'MMPENCIL', 'MMREPEAT', 'MMHAND', 'MMFOLD',
                       'MMONFLR', 'MMREAD', 'MMWRITE', 'MMDRAW', 'MMD', 'MML', 'MMR', 'MMO', 'MMW']

        for field in validFields:
            data.drop(data[(data[field] == '-1') & (data[field] == '')].index, inplace=True)
            data.loc[data[field] != '1', field] = 0
            data[field] = pd.to_numeric(data[field])

        data["MMSCORE"] = data[validFields].sum(axis=1)
        self.data = data
