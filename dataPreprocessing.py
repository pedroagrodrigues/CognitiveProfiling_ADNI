# Load data from database:
from database import getLabels, getColumn, dbConnect

# path = './dataFiles/dataConfirmation'

# try:
#     data = panda.read_pickle(path + '.pickle')
# except:
#     labelsToRemove = ['_id','directory_id', 'Subject', 'RID', 'Image_Data_ID', 'Modality', 'Visit', 'Acq_Date', 'EXAMDATE']
#     # this field is the object id generated from MongoDB, we dont need it.
#     labels = [label for label in getLabels() if label not in labelsToRemove]

#     # Saving into a file just to increase performance while debugging.
#     data = panda.DataFrame({label : getColumn(label) for label in labels})
#     data.to_pickle(path + '.pickle')
#     data.to_csv(path + '.csv')


# print(data['DX_bl'].value_counts())