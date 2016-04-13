import pandas as pd
import time
import datetime
import os

dataPath = "D:/Google Drive/PythonCodes/Data-Mining-Project--Walmart-Weekly-Forecast/data/"
dataFileNames = ["historical_features.csv", "train.csv"]

def read_pickled_data() -> dict:
    dataDict = {}
    for fileName in dataFileNames:
        dataName = os.path.splitext(fileName)[0]
        dataFrame = pd.read_pickle(dataName + "_pickled")
        dataDict[dataName] = dataFrame

    return dataDict


def pickle_data(dataToPickle: dict):
    for fileName in dataFileNames:
        dataName = os.path.splitext(fileName)[0]
        dataToPickle[dataName].to_pickle(dataName + "_pickled")

def dataFrameGen(fileName):

    dataFrame = pd.read_csv(dataPath + fileName, header = 0)

    #checking if a dataframe has a Date column
    if "Date" in dataFrame.columns.values:

        # if ture we are replacing the date column with an week number of the year
        #dateToWeekNumMap = {} #map dictionary for date mapping in a data frame
        # for loop to generate the map of values for the date column

        for row in dataFrame.iterrows():
            try:
                #print(row[1]["Date"])
                #dateToWeekNumMap[row["Date"]] = datetime.strptime(row["Date"],"%m/%d/%Y").strftime('%U')
                #print(time.strptime(row[1]["Date"],"%m/%d/%Y"))
                x=time.strptime(row[1]["Date"],"%m/%d/%Y")
                value = datetime.date(x.tm_year,x.tm_mon,x.tm_mday).isocalendar()[1]
                dataFrame.set_value(row[0],"Date", value)
            except Exception:
                pass
        #dataFrame["Date"] = dataFrame["Date"].map(dateToWeekNumMap)     #mapping the map to the dataframe to update
        dataFrame.rename(columns = {"Date":"WeekNum"}, inplace = True)  #updating the column name
    return dataFrame

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
    result.to_csv("train+features",index=False)


#pickle_data(dataRead())

merger()