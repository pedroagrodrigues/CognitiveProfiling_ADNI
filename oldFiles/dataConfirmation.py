# Load data from database:
from Database import Database
import json

    

def getMean(data):
    return round(sum(data)/len(data),1)

def getPercent(data, val):
    return round(data.count(val)/len(data) * 100,0)

credentials = json.load(open('credentials.json'))
db = Database("ADNI","ADNI_TQ1",credentials['user'], credentials['password'])

print("===============   TQ1   ===============")
print("Subjects in TQ1: ", len(db.query("RID")))
print("Subjects in CN: ", len(db.query("RID",{"DX_bl": "CN"})))
print("Subjects with  SMC: ", len(db.query("RID",{"DX_bl": "SMC"})))
print("Subjects with EMCI: ", len(db.query("RID",{"DX_bl": "EMCI"})))
print("Subjects with LMCI: ", len(db.query("RID",{"DX_bl": "LMCI"})))
print("Subjects with AD: ", len(db.query("RID",{"DX_bl": "AD"})))
print("Mean for MMSE baseline: ", getMean([eval(x["MMSE"]) for x in db.query({"VISCODE":'bl'},{"MMSE":1}, False)])) # 27.4
print("Mean for MMSE 24 months: ", getMean([eval(x["MMSE"]) for x in db.query({"VISCODE":'m24'},{"MMSE":1}, False)])) # 25.9
print("Mean for the age: ", getMean([eval(x["AGE"]) for x in db.query({"VISCODE":'bl'},{"AGE":1}, False)]))
print("Mean for years of education: ", getMean([eval(x["PTEDUCAT"]) for x in db.query({"VISCODE":'bl'},{"PTEDUCAT":1}, False)]))
print("Percentage of Females: ", getPercent([x["PTGENDER"] for x in db.query({"VISCODE": 'bl'},{"PTGENDER":1}, False)],"Female"), '%')
print("Percentage for APOE4 - 0: ", getPercent([x["APOE4"] for x in db.query({"VISCODE": 'bl'},{"APOE4":1}, False)],'0'), "%")
print("Percentage for APOE4 - 1: ", getPercent([x["APOE4"] for x in db.query({"VISCODE": 'bl'},{"APOE4":1}, False)],'1'), "%")
print("Percentage for APOE4 - 2: ", getPercent([x["APOE4"] for x in db.query({"VISCODE": 'bl'},{"APOE4":1}, False)],'2'), "%")


db.collection = "ADNI_TQ2"
print("\n")
print("===============   TQ2   ===============")
print("Subjects in TQ2 ", len(db.query("RID")))
print("All subjects present in this file are CN")
print("Mean for MMSE: ", getMean([eval(x["MMSE"]) for x in db.query({},{"MMSE":1}, False)])) 
print("Mean for years of education: ", getMean([eval(x["PTEDUCAT"]) for x in db.query({},{"PTEDUCAT":1}, False)]))
print("Percentage of Females: ", getPercent([x["PTGENDER"] for x in db.query({},{"PTGENDER":1}, False)],"Female"), '%')
print("Percentage for APOE4 - 0: ", getPercent([x["APOE4"] for x in db.query({},{"APOE4":1}, False)],'0'), "%")
print("Percentage for APOE4 - 1: ", getPercent([x["APOE4"] for x in db.query({},{"APOE4":1}, False)],'1'), "%")
print("Percentage for APOE4 - 2: ", getPercent([x["APOE4"] for x in db.query({},{"APOE4":1}, False)],'2'), "%")
print("Percentage for SAGE_Q2 - 0: ", getPercent([x["SAGE_Q2"] for x in db.query({},{"SAGE_Q2":1}, False)],'0'), "%")
print("Percentage for SAGE_Q2 - 1: ", getPercent([x["SAGE_Q2"] for x in db.query({},{"SAGE_Q2":1}, False)],'1'), "%")

db.collection = "ADNI_TQ3"

print("\n")
print("===============   TQ3   ===============")
print("Subjects in TQ3 ", len(db.query("RID")))
print("Subjects in CN: ", len(db.query("RID",{"DX_bl": "CN"})))
print("Subjects with LMCI: ", len(db.query("RID",{"DX_bl": "LMCI"})))
print("Subjects with AD: ", len(db.query("RID",{"DX_bl": "AD"})))
print("Mean for MMSE: ", getMean([eval(x["MMSE"]) for x in db.query({},{"MMSE":1}, False)])) 
print("Mean for the age: ", getMean([eval(x["AGE"]) for x in db.query({},{"AGE":1}, False)]))
print("Mean for years of education: ", getMean([eval(x["PTEDUCAT"]) for x in db.query({},{"PTEDUCAT":1}, False)]))
print("Percentage of Females: ", getPercent([x["PTGENDER"] for x in db.query({},{"PTGENDER":1}, False)],"Female"), '%')
print("Percentage for APOE4 - 0: ", getPercent([x["APOE4"] for x in db.query({},{"APOE4":1}, False)],'0'), "%")
print("Percentage for APOE4 - 1: ", getPercent([x["APOE4"] for x in db.query({},{"APOE4":1}, False)],'1'), "%")
print("Percentage for APOE4 - 2: ", getPercent([x["APOE4"] for x in db.query({},{"APOE4":1}, False)],'2'), "%")