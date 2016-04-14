# If you are new to python I just want to show you how we read data in python using pandas.
# I feel it always easy to work with data frames when we have ordered data like in our case.

''' Naming Conventions

Function names should be lowercase, with words separated by underscores as necessary to improve readability.

mixedCase is allowed only in contexts where that's already the prevailing style

Variables = camelCase

'''
from scipy import average
from read_data_functions import *
pd.options.mode.chained_assignment = None  # default='warn'


def week_mapping(deptStoreTestData,deptStoreTrainData,weekNum,weekType):
    weekDeptStoreTestData = deptStoreTestData[deptStoreTestData["WeekNum"] == weekNum]
    salesWeeklyDeptStoreTrainData = deptStoreTrainData[(abs(deptStoreTrainData["WeekNum"] - weekNum) < 2) & (deptStoreTrainData["IsHoliday"] == weekType)].Weekly_Sales
    weekDeptStoreTestData["Weekly_Sales"] = average(salesWeeklyDeptStoreTrainData)
    print(weekDeptStoreTestData)

def sales_mapping_rev1() -> list:
    testData = get_pickled_data_frame("test")
    trainData = get_pickled_data_frame("train")
    testData["Weekly_Sales"] = None
    #print(testData.head())
    #print(trainData.head())
    stores = list(set(testData.Store))

    for storeNum in stores:
        storeTestData = testData[testData["Store"] == storeNum]
        storeTrainData = trainData[trainData["Store"] == storeNum]
        depts = list(set(storeTestData.Dept))
        for deptNum in depts:
            deptStoreTestData = storeTestData[storeTestData["Dept"] == deptNum]
            deptStoreTrainData = storeTrainData[storeTrainData["Dept"] == deptNum]
            nonHolidayWeeks = list(set(deptStoreTestData[deptStoreTestData["IsHoliday"] == False].WeekNum))
            holidayWeeks = list(set(deptStoreTestData[deptStoreTestData["IsHoliday"] == True].WeekNum))
            for weekNum in nonHolidayWeeks:
                week_mapping(deptStoreTestData,deptStoreTrainData,weekNum,False)
                break
            for weekNum in holidayWeeks:
                week_mapping(deptStoreTestData,deptStoreTrainData,weekNum,True)
                break

            break
        break

sales_mapping_rev1()

