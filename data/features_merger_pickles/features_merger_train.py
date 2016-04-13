import pandas as pd
import time
import datetime
import os
from read_data_functions import *

dataPath = "D:/Google Drive/PythonCodes/Data-Mining-Project--Walmart-Weekly-Forecast/data/"
dataFileNames = ["historical_features.csv", "train.csv"]

def dataRead():

    data = {}
    for fileName in dataFileNames:
        dataName = os.path.splitext(fileName)[0]
        data[dataName] = dataFrameGen(fileName)
    return data


def merger():

    data = read_pickled_data()
    train = data["train"]
    histFeatures = data["historical_features"]
    result = pd.concat([train,histFeatures],axis=1)
    result.to_csv("train",index=False)


#pickle_data(dataRead())

merger()