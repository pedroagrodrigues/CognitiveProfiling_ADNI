import common

file = common.loadFile("Accuracy")
print(len(file[file.Accuracy.isna()].index.tolist()))

