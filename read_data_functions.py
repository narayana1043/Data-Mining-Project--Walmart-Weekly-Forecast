import os
import re
import pandas as pd
import time
from datetime import datetime
from sklearn import preprocessing
min_max_scaler = preprocessing.MinMaxScaler()


def read_pickled_data(dataPath, dataFileNames) -> dict:
    dataDict = {}
    for fileName in dataFileNames:
        dataName = os.path.splitext(fileName)[0]
        dataFrame = pd.read_pickle(dataPath + dataName + "_pickled")
        dataDict[dataName] = dataFrame

    return dataDict

def read_pickled_data_from_path(pickledFileBaseNames, path) -> dict:
    dataDict = {}
    for baseName in pickledFileBaseNames:
        dataDict[baseName] = get_pickled_data_frame(path + baseName + "_pickled")

    return dataDict

def get_pickled_data_frame(dataFrame):
    return pd.read_pickle("raw_frame_pickles/"+dataFrame+"_pickled")

def pickle_data(dataPath, dataFileNames, dataToPickle: dict):
    for fileName in dataFileNames:
        dataName = os.path.splitext(fileName)[0]
        dataToPickle[dataName].to_pickle(dataPath + dataName + "_pickled")

def pickle_data(pickleDataPath, dataToPickle: dict):
    for dataFrameName in dataToPickle.keys():
        print(dataToPickle[dataFrameName].head())
        dataToPickle[dataFrameName].to_pickle(pickleDataPath + dataFrameName + "_pickled")

#Reading data from files to generate a pandas data frame
def dataFrameGen(fileName,dataPath):
    dataFrame = pd.read_csv(dataPath + fileName, header = 0)
    if "Date" in dataFrame.columns.values:
        for row in dataFrame.iterrows():
            x = time.strptime(row[1]["Date"],"%m/%d/%Y")
            value = datetime(x.tm_year,x.tm_mon,x.tm_mday).isocalendar()[1]
            dataFrame.set_value(row[0],"Date", value)
        dataFrame.rename(columns = {"Date":"WeekNum"}, inplace = True)
    return dataFrame

#reading the files from locations and making a dictionary of data
def read_data() -> dict:
    dataPath = "data/"
    dataFileNames = ["stores.csv", "historical_features.csv", "future_features.csv", "train.csv"]
    data = {re.sub(r".csv","",file) : dataFrameGen(file,dataPath) for file in dataFileNames}
    return data

pickle_data("data/raw_frame_pickles/", read_data())