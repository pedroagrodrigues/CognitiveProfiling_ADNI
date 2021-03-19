# External imports
import numpy as np
import pandas as panda
import json

# Internal imports
from Database import Database

path = './dataFiles/MERGE'

try:
    data = panda.read_pickle(path+'.pickle')
except:
    credentials = json.load(open("credentials.json"))

    db = Database('ADNI', 'ADNIMERGE', credentials['user'], credentials['password'], credentials['server'])

    labelsToRemove = ['_id', 'PTRACCAT', 'update_stamp']
    # this field is the object id generated from MongoDB, we dont need it.
    labels = [label for label in db.getLabels() if label not in labelsToRemove]

    # Saving into a file just to increase performance while debugging.
    data = panda.DataFrame({label: db.getColumn(label) for label in labels})

    labelsToEval = ['AGE', 'PTEDUCAT', 'APOE4', 'FDG', 'PIB', 'AV45', 'CDRSB', 'ADAS11', 'ADAS13',
                    'ADASQ4', 'MMSE', 'RAVLT_immediate', 'RAVLT_learning', 'RAVLT_forgetting', 'RAVLT_perc_forgetting',
                    'LDELTOTAL', 'DIGITSCOR', 'TRABSCOR', 'FAQ', 'MOCA', 'EcogPtMem', 'EcogPtLang', 'EcogPtVisspat',
                    'EcogPtPlan', 'EcogPtOrgan', 'EcogPtDivatt', 'EcogPtTotal', 'EcogSPMem', 'EcogSPLang', 'EcogSPVisspat',
                    'EcogSPPlan', 'EcogSPOrgan', 'EcogSPDivatt', 'EcogSPTotal', 'IMAGEUID',
                    'Ventricles', 'Hippocampus', 'WholeBrain', 'Entorhinal', 'Fusiform', 'MidTemp', 'ICV', 'mPACCdigit',
                    'mPACCtrailsB', 'CDRSB_bl', 'ADAS11_bl', 'ADASQ4_bl', 'MMSE_bl', 'RAVLT_immediate_bl',
                    'RAVLT_learning_bl', 'RAVLT_forgetting_bl', 'RAVLT_perc_forgetting_bl', 'LDELTOTAL_BL', 'DIGITSCOR_bl',
                    'TRABSCOR_bl', 'FAQ_bl', 'mPACCdigit_bl', 'mPACCtrailsB_bl', 'Ventricles_bl',
                    'Hippocampus_bl', 'WholeBrain_bl', 'Entorhinal_bl', 'Fusiform_bl', 'MidTemp_bl', 'ICV_bl', 'MOCA_bl',
                    'EcogPtMem_bl', 'EcogPtLang_bl', 'EcogPtVisspat_bl', 'EcogPtPlan_bl', 'EcogPtOrgan_bl', 'EcogPtDivatt_bl',
                    'EcogPtTotal_bl', 'EcogSPLang_bl', 'EcogSPVisspat_bl', 'EcogSPPlan_bl', 'EcogSPOrgan_bl', 'EcogSPDivatt_bl',
                    'EcogSPTotal_bl', 'FDG_bl', 'PIB_bl', 'AV45_bl', 'Years_bl', 'Month_bl',
                    'Month', 'M']

    # data = [[eval(x) if x != '' else x for x in data[label]] for label in labelsToEval]

    # WARNING POSSIBLE DATA CHANGE!
    data['ABETA'] = [1700 if x == '>1700' else x for x in data['ABETA']]
    data['ABETA'] = [200 if x == '<200' else x for x in data['ABETA']]
    data['ABETA_bl'] = [1700 if x == '>1700' else x for x in data['ABETA_bl']]
    data['ABETA_bl'] = [200 if x == '<200' else x for x in data['ABETA_bl']]

    data['TAU'] = [1300 if x == '>1300' else x for x in data['TAU']]
    data['TAU'] = [80 if x == '<80' else x for x in data['TAU']]
    data['TAU_bl'] = [1300 if x == '>1300' else x for x in data['TAU_bl']]
    data['TAU_bl'] = [80 if x == '<80' else x for x in data['TAU_bl']]

    data['PTAU'] = [120 if x == '>120' else x for x in data['PTAU']]
    data['PTAU'] = [8 if x == '<8' else x for x in data['PTAU']]
    data['PTAU_bl'] = [120 if x == '>120' else x for x in data['PTAU_bl']]
    data['PTAU_bl'] = [8 if x == '8' else x for x in data['PTAU_bl']]

    data['FLDSTRENG'] = [eval(x.strip(' Tesla MRI')) if ' Tesla MRI' in x else x for x in data['FLDSTRENG']]

    # Labels:
    # CN        -> 0
    # MCI       -> 1
    # Dementia  -> 2
    data['DX'] = [0 if value == 'CN' else value for value in data['DX']]
    data['DX'] = [1 if value == 'MCI' else value for value in data['DX']]
    data['DX'] = [2 if value == 'Dementia' else value for value in data['DX']]
    # Labels:
    # CN        -> 0
    # LMCI      -> 1
    # EMCI      -> 2
    # AD        -> 3
    # SMC       -> 4
    data['DX_bl'] = [0 if value == 'CN' else value for value in data['DX_bl']]
    data['DX_bl'] = [1 if value == 'LMCI' else value for value in data['DX_bl']]
    data['DX_bl'] = [2 if value == 'EMCI' else value for value in data['DX_bl']]
    data['DX_bl'] = [3 if value == 'AD' else value for value in data['DX_bl']]
    data['DX_bl'] = [4 if value == 'SMC' else value for value in data['DX_bl']]

    data['PTGENDER'] = [1 if x == 'Male' else 0 for x in data['PTGENDER']]

    data['PTETHCAT'] = [0 if x == 'Not Hisp/Latino' else x for x in data['PTETHCAT']]
    data['PTETHCAT'] = [1 if x == 'Hisp/Latino' else x for x in data['PTETHCAT']]
    data['PTETHCAT'] = [2 if x == 'Unknown' else x for x in data['PTETHCAT']]

    data['PTMARRY'] = [0 if x == 'Unknown' else x for x in data['PTMARRY']]
    data['PTMARRY'] = [1 if x == 'Married' else x for x in data['PTMARRY']]
    data['PTMARRY'] = [2 if x == 'Widowed' else x for x in data['PTMARRY']]
    data['PTMARRY'] = [3 if x == 'Divorced' else x for x in data['PTMARRY']]
    data['PTMARRY'] = [4 if x == 'Never married' else x for x in data['PTMARRY']]
    
    
    data['PTRACCAT'] = [0 if x == 'White' else 1 for x in data['PTRACCAT']]

    data.to_pickle(path+'.pickle')
    data.to_csv(path+'.csv')

print(data['PTRACCAT'].value_counts())
print(data.head(10))

