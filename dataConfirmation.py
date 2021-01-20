# Load data from database:
from database import getLabels, getColumn, dbConnect


    

def getMean(data):
    return round(sum(data)/len(data),1)

def getPercent(data, val):
    return round(data.count(val)/len(data) * 100,0)


collection = dbConnect("ADNI","ADNI_TQ1")

print("===============   TQ1   ===============")
print("Subjects in TQ1: ", len(collection.distinct("RID")))
print("Subjects in CN: ", len(collection.distinct("RID",{"DX_bl": "CN"})))
print("Subjects with  SMC: ", len(collection.distinct("RID",{"DX_bl": "SMC"})))
print("Subjects with EMCI: ", len(collection.distinct("RID",{"DX_bl": "EMCI"})))
print("Subjects with LMCI: ", len(collection.distinct("RID",{"DX_bl": "LMCI"})))
print("Subjects with AD: ", len(collection.distinct("RID",{"DX_bl": "AD"})))
print("Mean for MMSE baseline: ", getMean([eval(x["MMSE"]) for x in collection.find({"VISCODE":'bl'},{"MMSE":1})])) # 27.4
print("Mean for MMSE 24 months: ", getMean([eval(x["MMSE"]) for x in collection.find({"VISCODE":'m24'},{"MMSE":1})])) # 25.9
print("Mean for the age: ", getMean([eval(x["AGE"]) for x in collection.find({"VISCODE":'bl'},{"AGE":1})]))
print("Mean for years of education: ", getMean([eval(x["PTEDUCAT"]) for x in collection.find({"VISCODE":'bl'},{"PTEDUCAT":1})]))
print("Percentage of Females: ", getPercent([x["PTGENDER"] for x in collection.find({"VISCODE": 'bl'},{"PTGENDER":1})],"Female"), '%')
print("Percentage for APOE4 - 0: ", getPercent([x["APOE4"] for x in collection.find({"VISCODE": 'bl'},{"APOE4":1})],'0'), "%")
print("Percentage for APOE4 - 1: ", getPercent([x["APOE4"] for x in collection.find({"VISCODE": 'bl'},{"APOE4":1})],'1'), "%")
print("Percentage for APOE4 - 2: ", getPercent([x["APOE4"] for x in collection.find({"VISCODE": 'bl'},{"APOE4":1})],'2'), "%")


collection = dbConnect("ADNI","ADNI_TQ2")

print("===============   TQ2   ===============")
print("Subjects in TQ2 ", len(collection.distinct("RID")))
print("All subjects present in this file are CN")
print("Mean for MMSE: ", getMean([eval(x["MMSE"]) for x in collection.find({},{"MMSE":1})])) 
print("Mean for years of education: ", getMean([eval(x["PTEDUCAT"]) for x in collection.find({},{"PTEDUCAT":1})]))
print("Percentage of Females: ", getPercent([x["PTGENDER"] for x in collection.find({},{"PTGENDER":1})],"Female"), '%')
print("Percentage for APOE4 - 0: ", getPercent([x["APOE4"] for x in collection.find({},{"APOE4":1})],'0'), "%")
print("Percentage for APOE4 - 1: ", getPercent([x["APOE4"] for x in collection.find({},{"APOE4":1})],'1'), "%")
print("Percentage for APOE4 - 2: ", getPercent([x["APOE4"] for x in collection.find({},{"APOE4":1})],'2'), "%")
print("Percentage for SAGE_Q2 - 0: ", getPercent([x["SAGE_Q2"] for x in collection.find({},{"SAGE_Q2":1})],'0'), "%")
print("Percentage for SAGE_Q2 - 1: ", getPercent([x["SAGE_Q2"] for x in collection.find({},{"SAGE_Q2":1})],'1'), "%")

collection = dbConnect("ADNI","ADNI_TQ3")

print("===============   TQ2   ===============")
print("Subjects in TQ3 ", len(collection.distinct("RID")))
print("Subjects in CN: ", len(collection.distinct("RID",{"DX_bl": "CN"})))
print("Subjects with LMCI: ", len(collection.distinct("RID",{"DX_bl": "LMCI"})))
print("Subjects with AD: ", len(collection.distinct("RID",{"DX_bl": "AD"})))
print("Mean for MMSE: ", getMean([eval(x["MMSE"]) for x in collection.find({},{"MMSE":1})])) 
print("Mean for the age: ", getMean([eval(x["AGE"]) for x in collection.find({},{"AGE":1})]))
print("Mean for years of education: ", getMean([eval(x["PTEDUCAT"]) for x in collection.find({},{"PTEDUCAT":1})]))
print("Percentage of Females: ", getPercent([x["PTGENDER"] for x in collection.find({},{"PTGENDER":1})],"Female"), '%')
print("Percentage for APOE4 - 0: ", getPercent([x["APOE4"] for x in collection.find({},{"APOE4":1})],'0'), "%")
print("Percentage for APOE4 - 1: ", getPercent([x["APOE4"] for x in collection.find({},{"APOE4":1})],'1'), "%")
print("Percentage for APOE4 - 2: ", getPercent([x["APOE4"] for x in collection.find({},{"APOE4":1})],'2'), "%")