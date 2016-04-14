# If you are new to python I just want to show you how we read data in python using pandas.
# I feel it always easy to work with data frames when we have ordered data like in our case.

''' Naming Conventions

Function names should be lowercase, with words separated by underscores as necessary to improve readability.

mixedCase is allowed only in contexts where that's already the prevailing style

Variables = camelCase

'''

from scipy import average

from constants import *
from read_data_functions import *
from sams_work.oop_objects import Store

def read_pickled_data() -> dict:
    dataDict = {}
    for fileName in DATA_FILE_NAMES:
        dataName = os.path.splitext(fileName)[0]
        dataFrame = pd.read_pickle(DATA_PATH + dataName + "_pickled")
        dataDict[dataName] = dataFrame

    return dataDict


def pickle_data(dataToPickle: dict):
    for fileName in DATA_FILE_NAMES:
        dataName = os.path.splitext(fileName)[0]
        dataToPickle[dataName].to_pickle(DATA_PATH + dataName + "_pickled")


#Reading data from files to generate a pandas data frame
def dataFrameGen(fileName):

    dataFrame = pd.read_csv(DATA_PATH + fileName, header = 0)

    #checking if a dataframe has a Date column

    if "Date" in dataFrame.columns.values:

        # if ture we are replacing the date column with an week number of the year
        # map dictionary for date mapping in a data frame

        dateToWeekNumMap = {}

        # for loop to generate the map of values for the date column

        for index,row in dataFrame.iterrows():
            try:
                dateToWeekNumMap[row["Date"]] = int(datetime.strptime(row["Date"],"%m/%d/%Y").strftime('%U'))
            except Exception:
                pass

        #mapping the map to the dataframe for update
        #updating the column name

        dataFrame["Date"] = dataFrame["Date"].map(dateToWeekNumMap)
        dataFrame.rename(columns = {"Date":"WeekNum"}, inplace = True)
    return dataFrame



#Example usage for pickling
#pickle_data(read_data_from_file())

#Example usage for unpickling
def read_data_from_pickle() -> dict:
    data = read_pickled_data()
    #print(data.keys())
    return data

def near_mean_cal(record,trainData):
    record["Weekly_Sales"] = average(trainData.loc[(trainData["Store"]==record["Store"]) & (trainData["Dept"]==record["Dept"]) & (abs(trainData["WeekNum"] - record["WeekNum"]) < 2)]["Weekly_Sales"])


def get_adjacent_week_sales_values(deptTrainData, record):
    return deptTrainData.loc[(abs(deptTrainData["WeekNum"] - record["WeekNum"]) < 2) & (deptTrainData["IsHoliday"] == record["IsHoliday"])]["Weekly_Sales"]


def sales_mapping():
    data = read_data_from_pickle()
    testData = data["test"]
    trainData = data["train"]
    testData["Weekly_Sales"] = None

    # this loop needs to be threaded.
    # for index,record in testData.iterrows():
    #     print(index)
    #     record["Weekly_Sales"] = average(trainData.loc[(trainData["Store"]==record["Store"]) & (trainData["Dept"]==record["Dept"]) & (abs(trainData["WeekNum"] - record["WeekNum"]) < 2)]["Weekly_Sales"])

    newTrainData = pd.DataFrame(columns=trainData.columns.values)
    newTrainData["Weekly_Sales_Averaged"] = None

    for storeNum in range(1, NUM_STORES + 1):
        print("Store: ", storeNum)
        storeTrainData = trainData[trainData["Store"] == storeNum]
        for deptNum in range(1, NUM_DEPTS + 1):
            print("Dept: ", deptNum)
            deptTrainData = storeTrainData[trainData["Dept"] == deptNum]
            for index, record in deptTrainData.iterrows():
                valuesToAverage = deptTrainData.loc[(abs(deptTrainData["WeekNum"] - record["WeekNum"]) < 2) & (deptTrainData["IsHoliday"] == record["IsHoliday"])]["Weekly_Sales"]
                deptTrainData.set_value(index, "Weekly_Sales_Averaged", average(valuesToAverage))

            newTrainData = newTrainData.append(deptTrainData)

    trainData = newTrainData

    print(testData.head())
