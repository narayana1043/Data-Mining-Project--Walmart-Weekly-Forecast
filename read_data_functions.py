import pandas as pd
import time
from datetime import datetime

"""
This file contains all the functions that let us read data from various files as per requirements.
In most cases files are picked and saved for faster access and code is written to access the pickles to perform read operations instead of the file.
The dataFrameGen in this file also is used to produce the pandas dataframes required for a given input file,further the dataframes are also stored as pickles.
"""

def read_pickled_data(dataFileNames) -> dict:
    dataDict = {}
    for fileName in dataFileNames:
        dataDict[fileName] = get_pickled_data_frame(fileName)
    return dataDict

def get_pickled_data_frame(dataName):
    return pd.read_pickle("pickles/"+dataName+"_pickled")

def pickle_data_frame(dataName, dataToPickle):
    dataToPickle.to_pickle("pickles/" + dataName + "_pickled")

def pickle_data(dataToPickle: dict):
    for dataFrameName in dataToPickle.keys():
        pickle_data_frame(dataFrameName,dataToPickle[dataFrameName])
        # dataToPickle[dataFrameName].to_pickle(pickleDataPath + dataFrameName + "_pickled")

#Reading data from files to generate a pandas data frame
def dataFrameGen(fileName,dataPath):
    dataFrame = pd.read_csv(dataPath + fileName, header = 0, low_memory=False)
    dataFrame["WeekNum"] = None
    if "Date" in dataFrame.columns.values:
        for row in dataFrame.iterrows():
            x = time.strptime(row[1]["Date"],"%m/%d/%Y")
            value = datetime(x.tm_year,x.tm_mon,x.tm_mday).isocalendar()[1]
            dataFrame.set_value(row[0],"WeekNum", value)
        #dataFrame.rename(columns = {"Date":"WeekNum"}, inplace = True)
    return dataFrame

#reading the files from locations and making a dictionary of data
def read_data(dataFileNames) -> dict:
    dataPath = "data/"
    data = {file : dataFrameGen(file+".csv",dataPath) for file in dataFileNames}
    pickle_data(data)

#read_data(["historical_features","test","train"])
#read_data(["stores"])