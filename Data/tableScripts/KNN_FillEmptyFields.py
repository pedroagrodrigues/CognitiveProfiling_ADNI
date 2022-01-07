# This file has the goal of filling the dataset that is missing data. We are naming it  "filledData"

import pandas as pd
import numpy as np
import math
from alive_progress import alive_bar

import threading
import queue


import common
from Data import JoinedData


class Calc:
    def __init__(self, number_threads: int):
        self.KNNnumber = 5
        self.mutex = threading.Lock()  # same as Semaphore started at 1
        self.stepComplete = 0  # Variable used for the progress bar
        self.number_threads = number_threads  # Number of tasks in parallel
        self.queue = queue.Queue()  # Queue to complete all tasks

        # ----- Initializing ----
        self.fillQueue()
        self.startThreads()

    def readFile(self) -> pd.DataFrame:
        return common.loadFile("filledData")

    # To prevent multiple writes on the file at the same time, we will use a semaphore
    def writeResult(self, row: pd.DataFrame, index: int) -> None:
        """Saves the result to a file

        Args:
            row (pd.DataFrame): Row with all data to save
            index (int): index of the row
        """
        # Reading and wrinting the file in this case is a critical part of the code, mutex will prevent parallel writing
        self.mutex.acquire()

        filledData = self.readFile()
        filledData.iloc[index] = row
        common.saveFile(filledData, "filledData")

        self.mutex.release()

    def getTasks(self) -> list:
        """This method gets all the tasks that are missing in the file
            This class saves every result on a file, this method will allow to
            restart from the last save allowing the processing to be interrupted

        Returns:
            list: Tasks yet to be complete
        """
        self.mutex.acquire()
        file = self.readFile()
        self.mutex.release()
        file = file.iloc[file.isnull().sum(1).sort_values(ascending=True).index]
        return [index for index, row in file.iterrows() if row.isnull().any()]  # Returns the indexes of NaNs

    def task(self) -> None:
        while not self.queue.empty():  # Keeps the task alive untill the queue runs out of tasks
            index = self.queue.get(block=True, timeout=0.05)
            res = fillNanVals(cleanData, allData, self.KNNnumber, index)
            self.writeResult(res, index)
            self.stepComplete += 1
            self.queue.task_done()

    def startThreads(self) -> None:
        # Creates workers for each work, bar is the thread for the progress bar, the others are the tasks to calculate for each missing columns
        bar = threading.Thread(target=self.updater)
        bar.start()
        threads = [threading.Thread(target=self.task, daemon=True) for _ in range(self.number_threads)]
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

    # A progress bar
    def updater(self) -> None:
        current = 0
        with alive_bar(self.qsize, title="Processing: ") as bar:
            while current < self.qsize:
                if current < self.stepComplete:
                    current += 1
                    bar()


# Loading Data
cleanData = common.loadFile("CleanedData").drop(
    ['RID', 'VISCODE', 'PTEDUCAT', 'PTGENDER', 'AGE'], axis=1)  # Dropping fields not used
allData = JoinedData().data.drop_duplicates()

# Preparing DataSets
allData = allData.drop([x for x in list(allData) if x not in list(cleanData)], axis=1)  # Drops fields that don't exist in cleanData
# Remove rows without diagnosis (This is the field we use to validate)
allData = allData[(allData.DX.notna()) & (allData.DX != '')]
allData = pd.merge(allData, cleanData, how="left", indicator=True).query("_merge != 'both'").drop(
    '_merge', axis=1).reset_index(drop=True)  # Removing cleanData rows from allData
allData.replace('', np.NaN, inplace=True)  # Remove empty string values with np.NaN to make it easier to detect later

allData = allData.astype("float")
cleanData = cleanData.astype("float")


# Loading Creating new Dataset
try:
    filledData = common.loadFile("filledData")
except:
    filledData = pd.DataFrame(np.nan, index=range(len(list(allData.index))), columns=allData.columns.to_list())
    common.saveFile(filledData, "filledData")


def distance(a, b):
    return math.sqrt((a - b)**2)

def distance(a: pd.DataFrame, b: pd.DataFrame, cols: list) -> float:
    # Using Euclidean Distance sqrt((a-b)**2)
    return float(np.linalg.norm(a[cols].values - b[cols].values, axis=1))

# Filling function
def fillNanVals(completeDataset: pd.DataFrame, dataToFill: pd.DataFrame, k: int, index: int) -> list:
    """Searches the mean from the k nearest evaluations

    Args:
        goodData (pd.DataFrame): dataframe without missing values
        dataToFill (pd.DataFrame): dataFrame from where we will index
        k (int): number of neighbours to consider
        index (int): the idex of the row to fill

    Returns:
        list: row with data filled

    """
    currentRow = dataToFill.iloc[[index]]

    labelsToFill = [x for x in list(currentRow) if currentRow[x].isna().all()]

    if not labelsToFill:
        return currentRow

    distanceLabels = [label for label in currentRow.columns if label not in labelsToFill]
    
    data = pd.DataFrame()
    data['TOTALS'] = completeDataset.drop(labelsToFill, axis=1).apply(lambda y: distance(y, currentRow, distanceLabels), axis=1)
    for label in labelsToFill:
        data[label] = completeDataset[label]
    data = data.sort_values(by=["TOTALS"])[:k]

    result = data[labelsToFill].mean()

    for label in labelsToFill:
        currentRow[label] = result[label]

    return currentRow


Calc(20)
