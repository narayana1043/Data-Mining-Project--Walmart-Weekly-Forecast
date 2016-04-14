"""

Spliting the data into holiday and non hoilday so that we can deal with independently

"""

from read_data_functions import *

def data_splitter():
    dataFrameNames = ["test","train_features_mixture"]
    data = read_pickled_data(dataFrameNames)
    for fileName in dataFrameNames:
        file2Split = data[fileName]
        holidayFile = file2Split[file2Split["IsHoliday"] == True]
        nonHolidayFile = file2Split[file2Split["IsHoliday"] == False]
        holidayFile.to_csv("data/holiday_data/"+fileName,index=False)
        nonHolidayFile.to_csv("data/non_holiday_data/"+fileName,index=False)

data_splitter()
