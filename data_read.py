# If you are new to python I just want to show you how we read data in python using pandas.
# I feel it always easy to work with data frames when we have ordered data like in our case.

''' Naming Conventions

Function names should be lowercase, with words separated by underscores as necessary to improve readability.

mixedCase is allowed only in contexts where that's already the prevailing style

Variables = camelCase

'''

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


def pickle_data(dataToPickle: dict):
    for fileName in dataFileNames:
        dataName = os.path.splitext(fileName)[0]
        dataToPickle[dataName].to_pickle(dataPath + dataName + "_pickled")


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
        train.Temperature[(train['Store'] == Store) & (train['WeekNum'] == WeekNum)] = Temperature
    return data

#Example usage for pickling/unpickling
#pickle_data(read_data())

def normalize():
    #reading pickle data
    data = read_pickled_data()
    train = data['train']
    print(train.head())
    #min max normalization for temperatures
    #train['Temperature'] = min_max_scaler.fit_transform(train['Temperature'])
    #min max normalization for sales
    #train['Weekly_Sales'] = min_max_scaler.fit_transform(train['Weekly_Sales'])
    for storeNum in range(1,46):
        for deptNum in range(1,100):
            pearsonCorr = abs(pearsonr(train.Weekly_Sales[(train['Dept'] == storeNum) & (train['Store'] == deptNum)],(train.Temperature[(train['Dept'] == storeNum) & (train['Store'] == deptNum)]))[0])
            if pearsonCorr > 0.8:
                print(storeNum,",",deptNum,",",pearsonCorr)

""" *************for ploting correaltion**************************
    for store in range(1,46):
        for dept in range(1,100):
            x = train.Weekly_Sales[(train['Dept'] == dept) & (train['Store'] == store)]
            y = train.Temperature[(train['Dept'] == dept) & (train['Store'] == store)]
            plt.scatter(x,y)
    plt.text(6, 1.5, 'Each data point denotes a department in a store for a particular date', style='italic',fontsize=10,bbox={'facecolor':'grey', 'alpha':0.5, 'pad':10})
    plt.title('Scatter plot to figure out there exists a relation b/w sales and temperatures',fontsize=14)
    plt.xlabel("Weekly Sales")
    plt.ylabel("Temperatures")
    plt.show()
    *******************************************************************"""

normalize()