
if __name__ == "__main__":
    from common import *
else:
    from .common import *

labels = ['RID', 'VISCODE', 'PTEDUCAT']
merge = loadData("ADNIMERGE", labels)
print(merge.loc[(merge["RID"] == "5256") & (merge["VISCODE"] == 'm12')]["PTEDUCAT"])

