from numpy import save


if __name__ == "__main__":
    from common import *
else:
    from .common import *

class Demog:
    def __init__(self) -> None:
        self.name = "PTDEMOG"
        self.dataLoader()

    def dataLoader(self) -> None:
        try:
            self.data = loadFile(self.name)
        except:
            # labelsToRemove = ['_id', 'index', 'Phase', 'ID', 'SITEID', 'VISCODE', 'USERDATE', 'update_stamp']
            # labels = [label for label in getLabels(self.name) if label not in labelsToRemove]
            """
                At this point I am just getting the data we will be using. Feel free to go back to the lines above and get the full dataset
            """
            labels = ['RID', 'PTEDUCAT', "PTGENDER", 'PTDOBMM', 'PTDOBYY', 'USERDATE']

            data = loadData(self.name, labels)
            data.drop_duplicates(subset=['RID'], inplace=True)
            # self.fixCodes(data)
            self.fixGender(data)
            self.calculateAge(data)
            data = data.drop(['PTDOBMM', 'PTDOBYY', 'USERDATE'], axis=1)
            saveFile(data, self.name)
            self.data = data

    def fixGender(self, data: pd.DataFrame) -> None:
        data["PTGENDER"].replace({2:0}, inplace=True)

    def calculateAge(self, data: pd.DataFrame) -> None:
        age = lambda a, b, date: round((int(date[0]) + int(date[1])/12) - (a + b/12), 1)
        data["AGE"] = data.apply(lambda row: age(row['PTDOBYY'], row['PTDOBMM'], row['USERDATE'].split('-')), axis=1)
        


    def fixCodes(self, data: pd.DataFrame) -> None:
        data.rename(columns={"VISCODE2": "VISCODE"}, inplace=True)
        data["VISCODE"].replace({"sc": "bl"}, inplace=True)


# print(Demog().data)