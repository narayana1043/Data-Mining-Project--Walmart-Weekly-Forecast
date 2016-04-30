from scipy import average, sum
from read_data_functions import *
pd.options.mode.chained_assignment = None  # default='warn'

"""
This file contains the code the generates the outputs for various stores based on the trend Analysis.
The trend is detect by using assigning various weights according to the distance from the values that need to be predicted
Note: The weights are codeed dynamically and change accordingly which produce files accordingly onto the output2 folder.
"""

#

def weightedAverage(salesWeeklyDeptStoreTrainData,weekNum):
        histWeekDiffSales = []
        histWeekDiffSalesWeights = []
        for weekNumDiff in range(weekWindow):
            weekNumDiffSales = salesWeeklyDeptStoreTrainData[abs(salesWeeklyDeptStoreTrainData["WeekNum"] - weekNum) == weekNumDiff]
            weight = 1
            for temp in weekNumDiffSales.Weekly_Sales:
                histWeekDiffSales.append(temp * weight)
                histWeekDiffSalesWeights.append(weight)
                weight = weight + weightIncrement
        return sum(histWeekDiffSales)/sum(histWeekDiffSalesWeights)


def week_mapping_nonholiday(deptStoreTestData,deptStoreTrainData,weekNum,weekType,outputFrame):
    weekDeptStoreTestData = deptStoreTestData[deptStoreTestData["WeekNum"] == weekNum]
    salesWeeklyDeptStoreTrainData = deptStoreTrainData[(abs(deptStoreTrainData["WeekNum"] - weekNum) < weekWindow) & (deptStoreTrainData["IsHoliday"] == weekType)]
    weekDeptStoreTestData["Weekly_Sales"] = weightedAverage(salesWeeklyDeptStoreTrainData,weekNum)
    outputFrame = outputFrame.append(weekDeptStoreTestData)
    return outputFrame

def week_mapping_holiday(deptStoreTestData,deptStoreTrainData,weekNum,weekType,outputFrame):
    weekDeptStoreTestData = deptStoreTestData[deptStoreTestData["WeekNum"] == weekNum]
    salesWeeklyDeptStoreTrainData = deptStoreTrainData[(abs(deptStoreTrainData["WeekNum"] - weekNum) < weekWindow) & (deptStoreTrainData["IsHoliday"] == weekType)]
    weekDeptStoreTestData["Weekly_Sales"] = weightedAverage(salesWeeklyDeptStoreTrainData,weekNum)
    outputFrame = outputFrame.append(weekDeptStoreTestData)
    return outputFrame

def sales_mapping() -> list:
    testData = get_pickled_data_frame("test")
    trainData = get_pickled_data_frame("train")
    outputFrame = pd.DataFrame()
    testData["Weekly_Sales"] = None
    stores = list(set(testData.Store))
    start = time.time()
    for storeNum in stores:
        print(storeNum,time.time())
        storeTestData = testData[testData["Store"] == storeNum]
        storeTrainData = trainData[trainData["Store"] == storeNum]
        depts = list(set(storeTestData.Dept))
        for deptNum in depts:
            deptStoreTestData = storeTestData[storeTestData["Dept"] == deptNum]
            deptStoreTrainData = storeTrainData[storeTrainData["Dept"] == deptNum]
            nonHolidayWeeks = list(set(deptStoreTestData[deptStoreTestData["IsHoliday"] == False].WeekNum))
            holidayWeeks = list(set(deptStoreTestData[deptStoreTestData["IsHoliday"] == True].WeekNum))
            for weekNum in nonHolidayWeeks:
                outputFrame=week_mapping_nonholiday(deptStoreTestData,deptStoreTrainData,weekNum,False,outputFrame)

            for weekNum in holidayWeeks:
                outputFrame=week_mapping_holiday(deptStoreTestData,deptStoreTrainData,weekNum,True,outputFrame)

    outputFrame.to_csv("data/output1/trendWeight"+str(weightIncrement)+".csv",index=False)
    pickle_data_frame("weightedWindowLT"+str(weekWindow),outputFrame)
    print(time.time() - start)


for i in [3,4,5,6,7,8,15,21,25,29,49]:
    weightIncrement = i
    weekWindow = 2
    sales_mapping()