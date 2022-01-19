import pandas as pd
import numpy as np

from alive_progress import alive_bar

import threading, multiprocessing
from multiprocessing import Queue, Value

from multiprocessing.spawn import freeze_support

import common

if __name__ == '__main__':
    freeze_support()

allData = common.loadFile("JoinedData") 
cleanData = common.loadFile("CleanedData").drop(
    ['RID', 'VISCODE', 'PTEDUCAT', 'PTGENDER', 'AGE'], axis=1) # Droping unused fields

allData = allData.drop([x for x in list(allData) if x not in list(cleanData)], axis=1)  # Drops fields that don't exist in cleanData

# Remove rows without diagnosis (This is the field we use to validate)
allData = allData[(allData.DX.notna()) & (allData.DX != '')]
allData = pd.merge(allData, cleanData, how="left", indicator=True).query("_merge != 'both'").drop('_merge', axis=1).reset_index(drop=True)  # Removing cleanData rows from allData
allData.replace('', np.NaN, inplace=True)  # Remove empty string values with np.NaN to make it easier to detect later

allData = allData.astype("float")
cleanData = cleanData.astype("float")


class Accuracy:
    def __init__(self) -> None:
        self.KNNnumber = 5
        self.mutex = multiprocessing.Lock() # Will use a semaphore started at 1 to prevent paralel writing

        self.stepComplete = Value('i', 0) # An updater for the progress bar
        self.fileName = "Accuracy"
        #self.number_threads = number_threads # Number of threads to use
        self.queue = Queue() 
        self.number_processors = multiprocessing.cpu_count()
        # self.data = file = pd.read_pickle(self.fileName)

        # ----- Processing -----
        self.fillQueue()

        if self.qsize != 0:
            self.startProcessing()

    def fillQueue(self) -> None:
        # Places all indexes to be calculated on the queue
        tasks = self.getTasks()
        self.qsize = len(tasks)
        for i in tasks:
            self.queue.put(i)
    
    def getTasks(self) -> list:
        # Gets the indexes of all lines yet to be calculated
        # Since this class takes arround 72 hours to complete for 189 tasks, we are saving each step.
        # This way we can cancel or stop the algorithm and pick up where we've left of
        self.mutex.acquire()
        file = self.readFile()
        self.mutex.release()
        return file[file.Accuracy.isna()].index.tolist()  # Returns the indexes of NaNs

    def readFile(self) -> pd.DataFrame:
        try:
            accuracy = common.loadFile(self.fileName)
        except:
            accuracy = pd.DataFrame(np.nan, index=range(max(allData.isnull().sum(axis=1))), columns=["Accuracy"])
            common.saveFile(accuracy, self.fileName)
        return accuracy

    def saveFile(self, data:pd.DataFrame) -> None:
        common.saveFile(data, self.fileName)
    
    def startProcessing(self) -> None:
        bar = threading.Thread(target=self.updater)
        processors = [multiprocessing.Process(target=self.task, daemon=True) for _ in range(self.number_processors)]
        bar.start()
        [process.start() for process in processors]
        [process.join() for process in processors]
        bar.join()

    def updater(self) -> None:
        # A simple progress bar to run on the main thread
        current = 0
        with alive_bar(self.qsize, title="Processing: ") as bar:
            while current < self.qsize:
                if current < self.stepComplete.value:
                    current += 1
                    bar()
    
    # def startThreads(self) -> None:
    #     threads = [threading.Thread(target=self.task, daemon=True) for _ in range(self.number_threads)]
    #     [thread.start() for thread in threads]
    #     [thread.join() for thread in threads]
    #     print("Im done here PID: ", multiprocessing.current_process().pid)

    def task(self) -> None:
        self.KNNnumber = 5  # Number of neighbours to count
        while not self.queue.empty():  # Keeps the task alive untill the queue runs out of tasks
            index = self.queue.get()
            res = incompleteFitting(cleanData, allData, self.KNNnumber, index)
            accuracy = res.count(True)/len(res) if len(res) != 0 else 0
            self.writeResult(accuracy, index)
            self.stepComplete.value += 1

    def writeResult(self, res: float, index: int) -> None:
        """Saves the result to a file

        Args:
            res (float): result from the row
            index (int): index of the row
        """
        self.mutex.acquire()
        # Reading and wrinting the file in this case is a critical part of the code, mutex will prevent parallel writing

        accuracy = self.readFile()
        accuracy.Accuracy[index] = res
        self.saveFile(accuracy)

        self.mutex.release()


def distance(a: pd.DataFrame, b: pd.DataFrame, cols: list) -> float:
    # Using Euclidean Distance sqrt((a-b)**2)
    return float(np.linalg.norm(a[cols].values - b[cols].values, axis=1))


# Function for incomplete fitting
def incompleteFitting(completeDataset: pd.DataFrame, incompleteData: pd.DataFrame, k: int, missingColumns: int) -> list:
    frequent = []
    # Drops rows with a number of nulls higher than missingColumns
    currentData = incompleteData.dropna(thresh=incompleteData.shape[1]-missingColumns, axis=0)
    for i in range(len(currentData)):
        currentRow = currentData.iloc[[i]]  # Gets the row of index i

        unusedLabels = [label for label in currentRow.columns if currentRow[label].isna().all()
                        ]  # Selects null values from this row
        unusedLabels.append('DX')  # Not using diagnostic for this calc (variable we want to compare)
        distanceLabels = [label for label in currentRow.columns if label not in unusedLabels]
        data = pd.DataFrame()
        data['TOTALS'] = completeDataset.drop(unusedLabels, axis=1).apply(
            lambda y: distance(y, currentRow, distanceLabels), axis=1)

        for label in unusedLabels:
            data[label] = completeDataset[label]

        best = list(data.sort_values(by=["TOTALS"]).DX[:k])
        frequent.append(max(set(best), key=best.count) == int(currentRow["DX"]))
    return frequent

if __name__ == '__main__':
    Accuracy()