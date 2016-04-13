from scipy import average

NUM_DEPTS = 99
NUM_STORES = 44
NUM_WEEKS = 52


class Store:

    def __init__(self, storeNum):
        self.departments = [None] * (NUM_DEPTS + 1)
        self.storeNum = storeNum
        self.initialize_depts()

    def initialize_depts(self):
        for deptNum in range(1, NUM_DEPTS + 1):
            self.departments[deptNum] = Dept(deptNum)

    def set_weekly_sales_averages(self, storeDataFrame):
        for deptNum in range(1, NUM_DEPTS + 1):
            print("Dept: ", deptNum)
            deptDataFrame = storeDataFrame[storeDataFrame["Dept"] == deptNum]
            self.departments[deptNum].set_weekly_sales_averages(deptDataFrame)


class Dept:

    def __init__(self, deptNum):
        self.deptNum = deptNum
        self.weekSaleAverages = [None] * (NUM_WEEKS + 1)
        self.initialize_week_sale_averages()

    def initialize_week_sale_averages(self):
        for weekNum in range(1, NUM_WEEKS + 1):
            self.weekSaleAverages[weekNum] = WeekSaleAverage()

    def set_weekly_sales_averages(self, deptDataFrame):
        for weekNum in range(1, NUM_WEEKS + 1):
            weekDataFrame = deptDataFrame[abs(deptDataFrame["WeekNum"] - weekNum) < 2]
            self.weekSaleAverages[weekNum].set_sale_averages(weekDataFrame)


class WeekSaleAverage:

    def __init__(self):
        self.holidaySalesAverage = None
        self.nonHolidaySalesAverage = None

    def set_sale_averages(self, weekDataFrame):
        holidaySalesValues = weekDataFrame.loc[weekDataFrame["IsHoliday"] == True]["Weekly_Sales"]
        nonHolidaySalesValues = weekDataFrame.loc[weekDataFrame["IsHoliday"] == False]["Weekly_Sales"]
        self.holidaySalesAverage = average(holidaySalesValues)
        self.nonHolidaySalesAverage = average(nonHolidaySalesValues)