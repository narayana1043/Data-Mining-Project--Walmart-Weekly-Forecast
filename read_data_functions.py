
import pandas as pd
import re
import os
from datetime import datetime
from sklearn import preprocessing
min_max_scaler = preprocessing.MinMaxScaler()
from matplotlib import pyplot as plt
from scipy.stats import pearsonr

dataPath = "data/"
dataFileNames = ["stores.csv", "historical_features.csv", "future_features.csv", "train.csv"]


def read_pickled_data() -> dict:
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

def get_pickled_data_frame(pickledDataFrameFullPath):
    return pd.read_pickle(pickledDataFrameFullPath)

def pickle_data(dataToPickle: dict):
    for fileName in dataFileNames:
        dataName = os.path.splitext(fileName)[0]
        dataToPickle[dataName].to_pickle(dataPath + dataName + "_pickled")

def pickle_data(pickleDataPath, dataToPickle: dict):

    for dataFrameName in dataToPickle.keys():
        dataToPickle[dataFrameName].to_pickle(pickleDataPath + dataFrameName + "_pickled")

#Reading data from files to generate a pandas data frame
def dataFrameGen(fileName):

    dataFrame = pd.read_csv(dataPath + fileName, header = 0)
    #checking if a dataframe has a Date column
    if "Date" in dataFrame.columns.values:
        # if ture we are replacing the date column with an week number of the year
        dateToWeekNumMap = {} #map dictionary for date mapping in a data frame
        for index,row in dataFrame.iterrows():# for loop to generate the map of values for the date column
            try:
                dateToWeekNumMap[row["Date"]] = datetime.strptime(row["Date"],"%m/%d/%Y").strftime('%U')
                value = datetime.strptime(row["Date"],"%m/%d/%Y").strftime('%U')
                row['Date'].update(row['date'], value)
            except Exception:
                pass
        dataFrame["Date"] = dataFrame["Date"].map(dateToWeekNumMap)     #mapping the map to the dataframe to update
        dataFrame.rename(columns = {"Date":"WeekNum"}, inplace = True)  #updating the column name
    return dataFrame

#reading the files from locations and making a dictionary of data
def read_data() -> dict:

    #creating a dictionary of data example data[stores] has data of the stores as dataframes defined by pandas
    data = {re.sub(r".csv","",file) : dataFrameGen(file) for file in dataFileNames}
    #displaying the first five lines of data from every file
    #this is only to cross check that everything works as per thoughts
    # for key,value in data.items():
    #     print(key)
    #     print(value.head(),"\n")
    train = data['train']
    train['Temperature'] = None
    historical_features = data['historical_features']
    #print(historical_features.head())
    for index,row in historical_features.iterrows():
        Store = row['Store']
        WeekNum = row['WeekNum']
        Temperature = row['Temperature']
        Fuel_Price = row['Fuel_Price']
        train.Temperature[(train['Store'] == Store) & (train['WeekNum'] == WeekNum)] = Temperature
        train['Temperature','Fuel_Price'][(train['Store'] == Store) & (train['WeekNum'] == WeekNum)] = [Temperature,Fuel_Price]
    return data


# def add_temp_and_fuel_price_to_train_data(trainDataFrame, historicalFeaturesDataFrame):
#     trainDataFrame['Temperature'] = None
#     trainDataFrame['Fuel_Price'] = None
#     # print(historical_features.head())
#     for index, row in historicalFeaturesDataFrame.iterrows():
#         print("Index ", index)
#         Store = row['Store']
#         WeekNum = row['WeekNum']
#         Temperature = row['Temperature']
#         Fuel_Price = row['Fuel_Price']
#         trainDataFrame.Temperature[(trainDataFrame['Store'] == Store) & (trainDataFrame['WeekNum'] == WeekNum)] = Temperature
#         trainDataFrame.Fuel_Price[(trainDataFrame['Store'] == Store) & (trainDataFrame['WeekNum'] == WeekNum)] = Fuel_Price
#         # trainDataFrame['Temperature'][(trainDataFrame['Store'] == Store) & (trainDataFrame['WeekNum'] == WeekNum)] = [Temperature, Fuel_Price]
#
#     return trainDataFrame