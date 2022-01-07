import pandas as pd 
import numpy as np
import math
from alive_progress import alive_bar


import threading, queue


import common
from Data import JoinedData


class incompleteCalc:
    def __init__(self, number_threads: int):
        self.KNNnumber = 5
        self.mutex = threading.Lock() # same as Semaphore started at 1
        self.stepComplete = 0 # Variable used for the progress bar
        self.number_threads = number_threads # Number of tasks in parallel
        self.queue = queue.Queue() # Queue to complete all tasks
        # ----- Initializing ----
        self.fillQueue()
        self.startThreads()
        
    
    def readFile(self) -> pd.DataFrame:
        return common.loadFile("Accuracy")

    def writeResult(self, res: float, index:int) -> None:
        """Saves the result to a file

        Args:
            res (float): result from the row
            index (int): index of the row
        """
        self.mutex.acquire()
        # Reading and wrinting the file in this case is a critical part of the code, mutex will prevent parallel writing

        accuracy = self.readFile()
        accuracy.Accuracy[index] = res
        common.saveFile(accuracy, "Accuracy")

        self.mutex.release()

    def getTasks(self) -> list:
        # Gets the indexes of all lines yet to be calculated
        # Since this class takes arround 72 hours to complete for 189 tasks, we are saving each step. 
        #This way we can cancel or stop the algorithm and pick up where we've left of
        self.mutex.acquire()
        file = self.readFile()
        self.mutex.release()
        return file[file.Accuracy.isna()].index.tolist() # Returns the indexes of NaNs


    def task(self) -> None:
        self.KNNnumber = 5 # Number of neighbours to count
        while not self.queue.empty(): # Keeps the task alive untill the queue runs out of tasks
            index = self.queue.get(block=True, timeout=0.05)
            res = incompleteFitting(cleanData, allData, self.KNNnumber, index)
            accuracy = res.count(True)/len(res) if len(res) != 0 else 0
            self.writeResult(accuracy, index)
            self.stepComplete += 1
            self.queue.task_done()


    def startThreads(self) -> None:
        # Creates workers for each work, bar is the thread for the progress bar, the others are the tasks to calculate for each missing columns
        bar = threading.Thread(target=self.updater)
        threads = [threading.Thread(target=self.task, daemon=True) for _ in range(self.number_threads)]
        bar.start()
        [thread.start() for thread in threads]
        [thread.join() for thread in threads]
        self.queue.join()
        bar.join()

    def fillQueue(self) -> None:
        # Places all indexes to be calculated on the queue
        tasks = self.getTasks()
        self.qsize = len(tasks)
        for i in tasks:
            self.queue.put(i)
        print(f"Queue size: {self.queue.qsize()}")
        
    # A progress bar
    def updater(self) -> None:
        print("Alive Bar Starting...\n")
        current = 0
        with alive_bar(self.qsize, title="Processing: ", force_tty=True) as bar:
            while current < self.qsize:
                if current < self.stepComplete:
                    current += 1
                    bar()
                time.sleep(10) # updates the bar each 10 secs - This task is not important so doesen't need to be always on the processor
    
    




# Loading Data
cleanData = common.loadFile("CleanedData").drop(['RID', 'VISCODE', 'PTEDUCAT', 'PTGENDER', 'AGE'], axis=1) # Dropping fields not used
allData = JoinedData().data.drop_duplicates()

allData = allData.drop([x for x in list(allData) if x not in list(cleanData)], axis=1) # Drops fields that don't exist in cleanData
allData = allData[(allData.DX.notna()) & (allData.DX != '')] # Remove rows without diagnosis (This is the field we use to validate)
allData = pd.merge(allData, cleanData, how="left", indicator=True).query("_merge != 'both'").drop('_merge', axis=1).reset_index(drop=True) # Removing cleanData rows from allData
allData.replace('', np.NaN, inplace=True) # Remove empty string values with np.NaN to make it easier to detect later

allData = allData.astype("float")
cleanData = cleanData.astype("float")

try:
    common.loadFile("Accuracy")
except:
    accuracy = pd.DataFrame(np.nan, index=range(max(allData.isnull().sum(axis=1))), columns=["Accuracy"])
    common.saveFile(accuracy, "Accuracy")

def distance(a: pd.DataFrame, b: pd.DataFrame, cols: list) -> float:
    # Using Euclidean Distance sqrt((a-b)**2)
    return float(np.linalg.norm(a[cols].values - b[cols].values, axis=1))

    

# Function for incomplete fitting
def incompleteFitting(completeDataset: pd.DataFrame, incompleteData: pd.DataFrame, k: int, missingColumns: int) -> list:
    frequent= []
    currentData = incompleteData.dropna(thresh=incompleteData.shape[1]-missingColumns, axis=0) # Drops rows with a number of nulls higher than missingColumns
    for i in range(len(currentData)):
        currentRow = currentData.iloc[[i]] # Gets the row of index i

        unusedLabels = [label for label in currentRow.columns if currentRow[label].isna().all()] # Selects null values from this row
        unusedLabels.append('DX') # Not using diagnostic for this calc (variable we want to compare)
        distanceLabels = [label for label in currentRow.columns if label not in unusedLabels]
        data = pd.DataFrame()
        data['TOTALS'] = completeDataset.drop(unusedLabels, axis=1).apply(lambda y: distance(y, currentRow, distanceLabels), axis=1)

        for label in unusedLabels:
            data[label] = completeDataset[label]

        best = list(data.sort_values(by=["TOTALS"]).DX[:k])
        frequent.append(max(set(best), key = best.count)==currentRow.DX)
    return frequent


incompleteCalc(50)