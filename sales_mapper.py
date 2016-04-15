from scipy import average
from read_data_functions import *
pd.options.mode.chained_assignment = None  # default='warn'


def week_mapping_naiveBayes(deptStoreTestData,deptStoreTrainData,weekNum,weekType,outputFrame):
    weekDeptStoreTestData = deptStoreTestData[deptStoreTestData["WeekNum"] == weekNum]
    salesWeeklyDeptStoreTrainData = deptStoreTrainData[(abs(deptStoreTrainData["WeekNum"] - weekNum) < weekWindow) & (deptStoreTrainData["IsHoliday"] == weekType)].Weekly_Sales
    weekDeptStoreTestData["Weekly_Sales"] = average(salesWeeklyDeptStoreTrainData)
    outputFrame = outputFrame.append(weekDeptStoreTestData)
    return outputFrame

def sales_mapping_naiveBayes() -> list:
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
                outputFrame = week_mapping_naiveBayes(deptStoreTestData,deptStoreTrainData,weekNum,False,outputFrame)

            for weekNum in holidayWeeks:
                outputFrame = week_mapping_naiveBayes(deptStoreTestData,deptStoreTrainData,weekNum,True,outputFrame)

    outputFrame.to_csv("data/output/NaiveBayesWindowLT"+str(weekWindow)+".csv",index=False)
    pickle_data_frame("NaiveBayesWindowLT"+str(weekWindow),outputFrame)
    print(time.time() - start)


# sales_mapping_naiveBayes()
# weekWindow = int(input("Please Enter the week window length"))

for i in range(3,5):
    weekWindow =i
    sales_mapping_naiveBayes()
