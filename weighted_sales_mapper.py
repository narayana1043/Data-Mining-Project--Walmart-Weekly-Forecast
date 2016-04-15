from scipy import average, sum
from read_data_functions import *
pd.options.mode.chained_assignment = None  # default='warn'


def weightedAverage(salesWeeklyDeptStoreTrainData,weekNum):
        histWeekDiffSales = []
        histWeekDiffSalesLen = []
        histWeekDiffSalesWeights = []
        numerator = 0
        denominator = 0
        for weekNumDiff in range(weekWindow):
            weekNumDiffSales = salesWeeklyDeptStoreTrainData[abs(salesWeeklyDeptStoreTrainData["WeekNum"] - weekNum) == weekNumDiff].Weekly_Sales
            try:
                histWeekDiffSalesWeights.append(1/(2*weekNumDiff))
                histWeekDiffSalesLen.append(len(weekNumDiffSales))
                histWeekDiffSales.append(histWeekDiffSalesWeights[weekNumDiff]*(weekNumDiffSales))
            except ZeroDivisionError:
                histWeekDiffSalesWeights.append(1)
                histWeekDiffSalesLen.append(len(weekNumDiffSales))
                histWeekDiffSales.append(sum(weekNumDiffSales))

        for weekNumDiff in range(weekWindow):
            numerator += sum(histWeekDiffSales[weekNumDiff])
            denominator += histWeekDiffSalesLen[weekNumDiff]*histWeekDiffSalesWeights[weekNumDiff]

        return (numerator/denominator)


def week_mapping(deptStoreTestData,deptStoreTrainData,weekNum,weekType,outputFrame):
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
                outputFrame=week_mapping(deptStoreTestData,deptStoreTrainData,weekNum,False,outputFrame)

            for weekNum in holidayWeeks:
                outputFrame=week_mapping(deptStoreTestData,deptStoreTrainData,weekNum,True,outputFrame)

    outputFrame.to_csv("data/output/weightedWindowLT"+weekWindow+".csv",index=False)
    pickle_data_frame("weightedWindowLT"+weekWindow,outputFrame)
    print(time.time() - start)

# weekWindow = int(input("Please Enter the week window length"))
# sales_mapping()

for i in range(3,5):
    weekWindow =i
    sales_mapping()