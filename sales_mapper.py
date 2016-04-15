from scipy import average
from read_data_functions import *
pd.options.mode.chained_assignment = None  # default='warn'

outputFrame = pd.DataFrame()
weekWindow = int(input("Please Enter the week window length"))


def week_mapping_navieBayes(deptStoreTestData,deptStoreTrainData,weekNum,weekType):
    weekDeptStoreTestData = deptStoreTestData[deptStoreTestData["WeekNum"] == weekNum]
    salesWeeklyDeptStoreTrainData = deptStoreTrainData[(abs(deptStoreTrainData["WeekNum"] - weekNum) < weekWindow) & (deptStoreTrainData["IsHoliday"] == weekType)].Weekly_Sales
    weekDeptStoreTestData["Weekly_Sales"] = average(salesWeeklyDeptStoreTrainData)
    outputFrame.append(weekDeptStoreTestData)

def sales_mapping_navieBayes() -> list:
    testData = get_pickled_data_frame("test")
    trainData = get_pickled_data_frame("train")
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
                week_mapping_navieBayes(deptStoreTestData,deptStoreTrainData,weekNum,False)
                break
            for weekNum in holidayWeeks:
                week_mapping_navieBayes(deptStoreTestData,deptStoreTrainData,weekNum,True)
                break
            break
        break
    outputFrame.to_csv("data/output/NavieBaseWindowLT3.csv",index=False)
    pickle_data_frame("OutputFrame",outputFrame)
    print(time.time() - start)


sales_mapping_navieBayes()

