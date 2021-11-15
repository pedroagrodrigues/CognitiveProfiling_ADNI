

if __name__ == "__main__":
    from common import *
else:
    from .common import *

from pandas.core.reshape.merge import merge
from Data import Mmse, Moca, Cdr, Merge, Ecogsp, Adas, Faq, Neurobat, Ecogpt, Merge, Demog

class JoinedData:
    """This class concatenates every NPA in one file
        You can use this class to address data just run once and use the file generated
    """
    def __init__(self) -> None:
        self.name = "JoinedData"
        self.dataLoader()

    def dataLoader(self) -> None:
        try:
            self.data = loadFile(self.name)
        except:
            npas = [Moca().data,  Mmse().data,  Adas().data, Cdr().data, Ecogsp().data, Faq().data, Neurobat().data, Ecogpt().data]
            npas.append(self.getDiagnosis())
            fieldsToDrop = ["ID", "SITEID", "Phase"]

            for i in range(len(npas)):
                for j in fieldsToDrop:
                    try:
                        npas[i] = npas[i].drop(j, axis=1)
                    except:
                        continue
            data = self.joinNpas(npas)
            data = self.getDemogData(data)
            data = data.drop_duplicates(subset=["RID", "VISCODE"], keep=False)
            saveFile(data, self.name)
            self.data = data

    def joinNpas(self, npas) -> pd.DataFrame:
        primaryKeys = ["RID", "VISCODE"]
        def aux(lst, data=0):
            if len(lst) == 0:
                return data
            if type(data) != pd.DataFrame:
                data = lst[0].set_index(primaryKeys)
                return aux(lst[1:], data)
            return aux(lst[1:], data.join(lst[0].set_index(primaryKeys)))
        return aux(npas)
   
    def getDemogData(self, data: pd.DataFrame) -> pd.DataFrame:
        """Get sociodemographics data

        Args:
            data (pd.DataFrame): Contains the data without sociodemographics

        Returns:
            pd.DataFrame: return the dataframe recieved with sociodemographics added
        """
        demog = Demog().data
        data = data.reset_index().set_index("RID")
        return data.join(demog.set_index("RID")).reset_index()
        
    def getDiagnosis(self) -> pd.DataFrame:
        """This will only load the diagnosis from the Merge file

        Returns:
            pd.DataFrame: Containing the data with RID, VISCODE and DX
        """
        res = Merge().data[["RID", "VISCODE", "DX"]]
        res["RID"] = pd.to_numeric(res["RID"])
        return res.dropna()
