
if __name__ == "__main__":
    from common import *
else:
    from .common import *


class Adas:
    def __init__(self) -> None:
        self.name = "ADAS"
        self.files = ["ADAS1TOTAL", "ADASGO23"]
        self.dataLoader()
        
    def dataLoader(self) -> pd.DataFrame:
        try:
            self.data = loadFile(self.name)
        except:
            self.Adni1()
            self.Adnigo23()
            self.data["RID"] = pd.to_numeric(self.data["RID"])
            saveFile(self.data, self.name)

    def Adni1(self) -> None:
        labels = getLabels(self.files[0])
        labelsToRemove = ["index", "_id", "EXAMDATE", "USERDATE", "USERDATE2", "update_stamp"]
        labels = [label for label in labels if label not in labelsToRemove]
        data = loadData(self.files[0], labels)
        data.rename(columns={"TOTAL11": "ADAS11", "TOTALMOD": "ADAS13"}, inplace=True)
        self.calculateTotals(data)
        data["Phase"] = "ADNI1"
        self.data = self.reorderData(data)

    def Adnigo23(self) -> None:
        labels = getLabels(self.files[1])
        labelsToRemove = ["_id", "EXAMDATE", "USERDATE", "USERDATE2", "update_stamp", "VISCODE", 'WORDLIST', 'Q1UNABLE', 'Q1TR1',
                            'Q1TR2', 'Q1TR3', 'Q1TRIT', 'Q1TR2T', 'Q1TRT', 'TIMEEND', 'Q2UNABLE', 'Q2TASK', 'Q3UNABLE',
                            'Q3TASK1', 'Q3TASK2', 'Q3TASK3', 'Q3TASK4', 'Q4UNABLE', 'TIMEBEGAN', 'Q4TASK', 'Q5UNABLE', 'Q5TASK',
                            'Q5SCORE_CUE', 'Q5NAME1', 'Q5NAME2', 'Q5NAME3', 'Q5NAME4', 'Q5NAME5', 'Q5NAME6', 'Q5NAME7', 'Q5NAME8',
                            'Q5NAME9', 'Q5NAME10', 'Q5NAME11', 'Q5NAME12', 'Q5FINGER', 'Q6UNABLE', 'Q6TASK', 'Q7UNABLE', 'Q7TASK',
                            'Q8UNABLE', 'Q8WORD1', 'Q8WORD1R', 'Q8WORD2', 'Q8WORD2R', 'Q8WORD3', 'Q8WORD3R', 'Q8WORD4', 'Q8WORD4R',
                            'Q8WORD5', 'Q8WORD5R', 'Q8WORD6', 'Q8WORD6R', 'Q8WORD7', 'Q8WORD7R', 'Q8WORD8', 'Q8WORD8R', 'Q8WORD9',
                            'Q8WORD9R', 'Q8WORD10', 'Q8WORD10R', 'Q8WORD11', 'Q8WORD11R', 'Q8WORD12', 'Q8WORD12R', 'Q8WORD13',
                            'Q8WORD13R', 'Q8WORD14', 'Q8WORD14R', 'Q8WORD15', 'Q8WORD15R', 'Q8WORD16', 'Q8WORD16R', 'Q8WORD17',
                            'Q8WORD17R', 'Q8WORD18', 'Q8WORD18R', 'Q8WORD19', 'Q8WORD19R', 'Q8WORD20', 'Q8WORD20R', 'Q8WORD21',
                            'Q8WORD21R', 'Q8WORD22', 'Q8WORD22R', 'Q8WORD23', 'Q8WORD23R', 'Q8WORD24', 'Q8WORD24R', 'Q9TASK',
                            'Q10TASK', 'Q11TASK', 'Q12TASK', 'Q13UNABLE', 'Q13TASKA', 'Q13TASKB', 'Q13TASKC', 'COMM']
        labels = [label for label in labels if label not in labelsToRemove]
        data = loadData(self.files[1], labels)
        self.fixNames(data)
        self.calculateTotals(data)
        self.data = self.data.append(self.reorderData(data), ignore_index=True)

    def fixNames(self, data: pd.DataFrame) -> None:
        names = {
            "VISCODE2": "VISCODE",
            "Q1SCORE": "Q1",
            "Q2SCORE": "Q2",
            "Q3SCORE": "Q3",
            "Q4SCORE": "Q4",
            "Q5SCORE": "Q5",
            "Q6SCORE": "Q6",
            "Q7SCORE": "Q7",
            "Q8SCORE": "Q8",
            "Q9SCORE": "Q9",
            "Q10SCORE": "Q10",
            "Q11SCORE": "Q11",
            "Q12SCORE": "Q12",
            "Q13SCORE": "Q14",  # This is changed to Q14 because on ADAS1 is there is no Q13, so this was adapted. Total dosent change
            "TOTSCORE": "ADAS11",
            "TOTAL13": "ADAS13"
        }
        data.rename(columns=names, inplace=True)
        

    def reorderData(self, data: pd.DataFrame) -> pd.DataFrame:
        return data.reindex(columns=["Phase", "ID", "RID", "SITEID", "VISCODE", "Q1", "Q2", "Q3",
                              "Q4", "Q5", "Q6", "Q7", "Q8", "Q9", "Q10", "Q11", "Q12", "Q14", "ADAS11", "ADAS13"])

    def calculateTotals(self, data: pd.DataFrame) -> None:
        ADAS11 = ["Q1", "Q2", "Q3", "Q5", "Q6", "Q7", "Q8", "Q9", "Q10", "Q11", "Q12"]
        ADAS13 = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "Q9", "Q10", "Q11", "Q12", "Q14"]
        for field in ADAS13:
            data[field] = pd.to_numeric(data[field])
        data["ADAS11"] = data[ADAS11].sum(axis=1)
        data["ADAS13"] = data[ADAS13].sum(axis=1)


# print(Adas().data.head())
