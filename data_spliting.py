"""

Spliting the data into holiday and non hoilday so that we can deal with independently

"""

import os
import pandas as pd


dataPath = "data/"
dataFileNames = ["stores.csv", "historical_features.csv", "future_features.csv", "train.csv","test.csv"]

def read_pickled_data() -> dict:

    dataDict = {}
    for fileName in dataFileNames:
        dataName = os.path.splitext(fileName)[0]
        dataFrame = pd.read_pickle(dataPath + dataName + "_pickled")
        dataDict[dataName] = dataFrame

    return dataDict


def pickle_data(dataToPickle: dict):

    for fileName in dataFileNames:
        dataName = os.path.splitext(fileName)[0]
        dataToPickle[dataName].to_pickle(dataPath + dataName + "_pickled")


#unpickling
def read_data_from_pickle() -> dict:

    data = read_pickled_data()
    #print(data.keys())
    return data

def data_splitter():

    data = read_data_from_pickle()
    for file in ["test","train"]:
        file2Split = data[file]
        holidayFile = file2Split[file2Split["IsHoliday"] == True]
        nonHolidayFile = file2Split[file2Split["IsHoliday"] == False]
        holidayFile.to_csv("data/holiday_data/"+file,index=False)
        nonHolidayFile.to_csv("data/non_holiday_data/"+file,index=False)

data_splitter()
