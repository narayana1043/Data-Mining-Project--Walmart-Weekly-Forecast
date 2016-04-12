# If you are new to python I just want to show you how we read data in python using pandas.
# I feel it always easy to work with data frames when we have ordered data like in our case.

''' Naming Conventions

Function names should be lowercase, with words separated by underscores as necessary to improve readability.

mixedCase is allowed only in contexts where that's already the prevailing style

Variables = camelCase

'''

import pandas as pd                 #using pandas module to work with dataframes
import re                           #using regular expressions to create dataframe names from the datafile names
from datetime import datetime       #using datetime module to convert dates into week numbers
import matplotlib as plt

#Reading data from files to generate a pandas data frame
def dataFrameGen(fileName):
    dataFrame = pd.read_csv("./data/"+fileName, header = 0)
    #checking if a dataframe has a Date column
    if "Date" in dataFrame.columns.values:
        # if ture we are replacing the date column with an week number of the year
        dateToWeekNumMap = {} #map dictionary for date mapping in a data frame
        for index,row in dataFrame.iterrows():# for loop to generate the map of values for the date column
            try:
                dateToWeekNumMap[row["Date"]] = datetime.strptime(row["Date"],"%Y-%m-%d").strftime('%U')
                value = datetime.strptime(row["Date"],"%Y-%m-%d").strftime('%U')
                row['Date'].update(row['date'], value)
            except Exception:
                pass
        dataFrame["Date"] = dataFrame["Date"].map(dateToWeekNumMap)   #mapping the map to the dataframe to update
        dataFrame.rename(columns = {"Date":"WeekNum"}, inplace = True)
        print(dataFrame.head())
    return dataFrame

#reading the files from locations and making a dictionary of data
def read_data():
    # data file names
    fileNames = ["stores.csv","features.csv","train.csv"]
    #creating a dictionary of data example data[stores] has data of the stores as dataframes defined by pandas
    stores = dataFrameGen(fileNames[0])
    features = dataFrameGen(fileNames[1])
    train = dataFrameGen(fileNames[2])
    print(stores.head())
    print(features.head())
    temp_dict = {}
    for index,row in features.iterrows():
         temp_dict[row["Store"],row["WeekNum"]]= row["Temperature"]
    #train["Temperature"] = train["Temperature","WeekNum"].map(temp_dict)
    #plt.scatter()
read_data()
