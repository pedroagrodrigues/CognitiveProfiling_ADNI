import numpy as np
import pandas as panda
import json
# Load data from database:
from Database import Database

path = './dataFiles/ADNI_MERGE'

try:
    data = panda.read_pickle(path+'.pickle')
except:
    credentials = json.load(open("credentials.json"))

    db = Database('ADNI', 'ADNIMERGE', credentials['user'], credentials['password'])

    labelsToRemove = ['_id', 'RID', 'PTID', 'SITE', 'COLPROT', 'ORIGPROT', 'PRID', 'EXAMDATE', 'EXAMDATE_bl', 'Years_bl', 'Month_bl', 'Month', 'M']
    # this field is the object id generated from MongoDB, we dont need it.
    labels = [label for label in db.getLabels() if label not in labelsToRemove]

    # Saving into a file just to increase performance while debugging.
    data = panda.DataFrame({label : db.getColumn(label) for label in labels})
    data.to_pickle(path+'.pickle')
    data.to_csv(path+'.csv') #easier to see

# data[targetLabel] = panda.get_dummies(data[targetLabel])

def getUniqueCategories(data):
    for col in data:
        if data[col].dtypes == 'object':
            unique = len(data[col].unique())
            print(f"Feature \033[33m '{col}' \033[0m has \033[33m {unique} \033[0m unique categories")


# DX labels will follow this rule:
# CN          ->  0
# LMCI        ->  1
# EMCI        ->  2
# AD          ->  3
# MCI         ->  4
# SMC         ->  5
# NA          ->  Del

data['VISCODE'] = [0 if x == 'bl' else int(x.replace('m','')) for x in data['VISCODE']]


data['DX_bl'] = [0 if x == 'CN' else x for x in data['DX_bl']]
data['DX_bl'] = [1 if x == 'LMCI' else x for x in data['DX_bl']]
data['DX_bl'] = [2 if x == 'EMCI' else x for x in data['DX_bl']]
data['DX_bl'] = [3 if x == 'AD' else x for x in data['DX_bl']]
data['DX_bl'] = [4 if x == 'MCI' else x for x in data['DX_bl']]
data['DX_bl'] = [5 if x == 'SMC' else x for x in data['DX_bl']]
idxRem = data.index[data['DX_bl'] == 'NA'].tolist() #indexes to delete

data['AGE'] = [eval(x) for x in data['AGE']]
data['PTGENDER'] = [1 if x == 'Male' else 0 for x in data['PTGENDER']]
data['PTEDUCAT'] = [eval(x) for x in data['PTEDUCAT']]
data['PTETHCAT'] = [1 if x == "Not Hisp/Latino" else 0 for x in data['PTETHCAT']]
data['PTRACCAT'] = [1 if x == "White" else 0 for x in data['PTRACCAT']]

data['PTMARRY'] = [1 if x == "Married" else x for x in data['PTMARRY']]
data['PTMARRY'] = [2 if x == "Widowed" else x for x in data['PTMARRY']]
data['PTMARRY'] = [3 if x == "Divorced" else x for x in data['PTMARRY']]
data['PTMARRY'] = [0 if x == "Never married" else x for x in data['PTMARRY']]
data['PTMARRY'] = [0 if x == "Unknown" else x for x in data['PTMARRY']]

data['APOE4'] = [0 if x == 'NA' else eval(x) for x in data['APOE4']]
data['FDG'] = [0 if x == 'NA' else eval(x) for x in data['FDG']]
data['PIB'] = [0 if x == 'NA' else eval(x) for x in data['PIB']]
data['AV45'] = [0 if x == 'NA' else eval(x) for x in data['AV45']]
data['CDRSB'] = [0 if x == 'NA' else eval(x) for x in data['CDRSB']]
data['ADAS11'] = [0 if x == 'NA' else eval(x) for x in data['ADAS11']]
data['ADAS13'] = [0 if x == 'NA' else eval(x) for x in data['ADAS13']]
data['MMSE'] = [0 if x == 'NA' else eval(x) for x in data['MMSE']]
data['RAVLT_immediate'] = [0 if x == 'NA' else eval(x) for x in data['RAVLT_immediate']]
data['RAVLT_learning'] = [0 if x == 'NA' else eval(x) for x in data['RAVLT_learning']]
data['RAVLT_forgetting'] = [0 if x == 'NA' else eval(x) for x in data['RAVLT_forgetting']]
data['RAVLT_perc_forgetting'] = [0 if x == 'NA' else eval(x) for x in data['RAVLT_perc_forgetting']]
data['FAQ'] = [0 if x == 'NA' else eval(x) for x in data['FAQ']]
data['MOCA'] = [0 if x == 'NA' else eval(x) for x in data['MOCA']]
data['EcogPtMem'] = [0 if x == 'NA' else eval(x) for x in data['EcogPtMem']]
data['EcogPtLang'] = [0 if x == 'NA' else eval(x) for x in data['EcogPtLang']]
data['EcogPtVisspat'] = [0 if x == 'NA' else eval(x) for x in data['EcogPtVisspat']]
data['EcogPtPlan'] = [0 if x == 'NA' else eval(x) for x in data['EcogPtPlan']]
data['EcogPtOrgan'] = [0 if x == 'NA' else eval(x) for x in data['EcogPtOrgan']]
data['EcogPtDivatt'] = [0 if x == 'NA' else eval(x) for x in data['EcogPtDivatt']]
data['EcogPtTotal'] = [0 if x == 'NA' else eval(x) for x in data['EcogPtTotal']]
data['EcogSPMem'] = [0 if x == 'NA' else eval(x) for x in data['EcogSPMem']]
data['EcogSPLang'] = [0 if x == 'NA' else eval(x) for x in data['EcogSPLang']]
data['EcogSPVisspat'] = [0 if x == 'NA' else eval(x) for x in data['EcogSPVisspat']]
data['EcogSPPlan'] = [0 if x == 'NA' else eval(x) for x in data['EcogSPPlan']]
data['EcogSPOrgan'] = [0 if x == 'NA' else eval(x) for x in data['EcogSPOrgan']]
data['EcogSPDivatt'] = [0 if x == 'NA' else eval(x) for x in data['EcogSPDivatt']]
data['EcogSPTotal'] = [0 if x == 'NA' else eval(x) for x in data['EcogSPTotal']]
data['Ventricles'] = [0 if x == 'NA' else eval(x) for x in data['Ventricles']]
data['Hippocampus'] = [0 if x == 'NA' else eval(x) for x in data['Hippocampus']]
data['WholeBrain'] = [0 if x == 'NA' else eval(x) for x in data['WholeBrain']]
data['Entorhinal'] = [0 if x == 'NA' else eval(x) for x in data['Entorhinal']]
data['Fusiform'] = [0 if x == 'NA' else eval(x) for x in data['Fusiform']]
data['MidTemp'] = [0 if x == 'NA' else eval(x) for x in data['MidTemp']]
data['ICV'] = [0 if x == 'NA' else eval(x) for x in data['ICV']]

data['DX'] = [3 if x == 'MCI to Dementia' or x == 'NL to Dementia' or x == 'Dementia' else x for x in data['DX']]
data['DX'] = [1 if x == 'NL to MCI' or x == 'Dementia to MCI' or x == 'MCI' else x for x in data['DX']]
data['DX'] = [2 if x == 'MCI to NL' or x == 'NL' else x for x in data['DX']]
data['DX'] = [0 if x == 'NA' else x for x in data['DX']]

data['CDRSB_bl'] = [eval(x) for x in data['CDRSB_bl']]
data['ADAS11_bl'] = [0 if x == 'NA' else eval(x) for x in data['ADAS11_bl']]
data['ADAS13_bl'] = [0 if x == 'NA' else eval(x) for x in data['ADAS13_bl']]
data['MMSE_bl'] = [eval(x) for x in data['MMSE_bl']]
data['RAVLT_immediate_bl'] = [0 if x == 'NA' else eval(x) for x in data['RAVLT_immediate_bl']]
data['RAVLT_learning_bl'] = [0 if x == 'NA' else eval(x) for x in data['RAVLT_learning_bl']]
data['RAVLT_forgetting_bl'] = [0 if x == 'NA' else eval(x) for x in data['RAVLT_forgetting_bl']]
data['RAVLT_perc_forgetting_bl'] = [0 if x == 'NA' else eval(x) for x in data['RAVLT_perc_forgetting_bl']]
data['FAQ_bl'] = [0 if x == 'NA' else eval(x) for x in data['FAQ_bl']]
data['Ventricles_bl'] = [0 if x == 'NA' else eval(x) for x in data['Ventricles_bl']]
data['Hippocampus_bl'] = [0 if x == 'NA' else eval(x) for x in data['Hippocampus_bl']]
data['WholeBrain_bl'] = [0 if x == 'NA' else eval(x) for x in data['WholeBrain_bl']]
data['Entorhinal_bl'] = [0 if x == 'NA' else eval(x) for x in data['Entorhinal_bl']]
data['Fusiform_bl'] = [0 if x == 'NA' else eval(x) for x in data['Fusiform_bl']]
data['MidTemp_bl'] = [0 if x == 'NA' else eval(x) for x in data['MidTemp_bl']]
data['ICV_bl'] = [0 if x == 'NA' else eval(x) for x in data['ICV_bl']]
data['MOCA_bl'] = [0 if x == 'NA' else eval(x) for x in data['MOCA_bl']]
data['EcogPtMem_bl'] = [0 if x == 'NA' else eval(x) for x in data['EcogPtMem_bl']]
data['EcogPtLang_bl'] = [0 if x == 'NA' else eval(x) for x in data['EcogPtLang_bl']]
data['EcogPtVisspat_bl'] = [0 if x == 'NA' else eval(x) for x in data['EcogPtVisspat_bl']]
data['EcogPtPlan_bl'] = [0 if x == 'NA' else eval(x) for x in data['EcogPtPlan_bl']]
data['EcogPtOrgan_bl'] = [0 if x == 'NA' else eval(x) for x in data['EcogPtOrgan_bl']]
data['EcogPtDivatt_bl'] = [0 if x == 'NA' else eval(x) for x in data['EcogPtDivatt_bl']]
data['EcogPtTotal_bl'] = [0 if x == 'NA' else eval(x) for x in data['EcogPtTotal_bl']]
data['EcogSPMem_bl'] = [0 if x == 'NA' else eval(x) for x in data['EcogSPMem_bl']]
data['EcogSPLang_bl'] = [0 if x == 'NA' else eval(x) for x in data['EcogSPLang_bl']]
data['EcogSPVisspat_bl'] = [0 if x == 'NA' else eval(x) for x in data['EcogSPVisspat_bl']]
data['EcogSPPlan_bl'] = [0 if x == 'NA' else eval(x) for x in data['EcogSPPlan_bl']]
data['EcogSPOrgan_bl'] = [0 if x == 'NA' else eval(x) for x in data['EcogSPOrgan_bl']]
data['EcogSPDivatt_bl'] = [0 if x == 'NA' else eval(x) for x in data['EcogSPDivatt_bl']]
data['EcogSPTotal_bl'] = [0 if x == 'NA' else eval(x) for x in data['EcogSPTotal_bl']]
data['FDG_bl'] = [0 if x == 'NA' else eval(x) for x in data['FDG_bl']]
data['PIB_bl'] = [0 if x == 'NA' else eval(x) for x in data['PIB_bl']]
data['AV45_bl'] = [0 if x == 'NA' else eval(x) for x in data['AV45_bl']]

print(data.head(5))
# print(data['RAVLT_learning_bl'].value_counts())



#### Target data setup:
### Fixing Labels
# Some of the subjects were between diagnosis. 
# Since they seem to be changing between two of 
# them, I've decided to consider the target of 
# this change, example if the diagnosis was MCI to 
# Dementia the model will treat this subject as Dementia.
# The alternative to this was to remove this row or to 
# create a new target like "other" 

# 'MCI to Dementia' -> 'Dementia'  (284)
# 'NL to MCI'       -> 'MCI'       (76)
# 'MCI to NL'       -> 'NL'        (57)
# 'Dementia to MCI' -> 'MCI'       (6)
# 'NL to Dementia'  -> 'Dementia'  (3)

# Also labels must be converted to a numeric value corresponding to their number
# 'NA'       -> 0
# 'MCI'      -> 1
# 'NL'       -> 2
# 'Dementia' -> 3
###



# targetLabel = 'DX'

# data[targetLabel] = [3 if value == 'MCI to Dementia' or value == 'NL to Dementia' or value == 'Dementia' else value for value in data[targetLabel]]
# data[targetLabel] = [1 if value == 'NL to MCI' or value == 'Dementia to MCI' or value == 'MCI' else value for value in data[targetLabel]]
# data[targetLabel] = [2 if value == 'MCI to NL' or value == 'NL' else value for value in data[targetLabel]]
# data[targetLabel] = [0 if value == 'NA' else value for value in data[targetLabel]]

# # X is the data, y is the target or value corresponding to this data
# x = data.drop(targetLabel, 1)
# y = data[targetLabel]

#Same process is applied to DX_bl





# for i in x:
#     print (f"Categories for \033[33m '{i}' \033[0m category")
#     print(x[i].value_counts())
#     input('press enter to proceed')

# getUniqueCategories(x)

