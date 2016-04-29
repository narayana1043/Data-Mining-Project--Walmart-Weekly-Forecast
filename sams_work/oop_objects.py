from enum import Enum

import numpy
from pandas.stats.api import ols

from sams_work.predictions_set_object import *

featureStringToNum = {
    "Temperature": 0,
    "Fuel_Price": 1,
    "MarkDown1":  2,
    "MarkDown2": 3,
    "MarkDown3": 4,
    "MarkDown4": 5,
    "MarkDown5": 6,
    "CPI": 7,
    "Unemployment": 8,
    "IsHoliday": 9
}

class Feature(Enum):
    Temperature = 0
    Fuel_Price = 1
    MarkDown1 = 2
    MarkDown2 = 3
    MarkDown3 = 4
    MarkDown4 = 5
    MarkDown5 = 6
    CPI = 7
    Unemployment = 8
    IsHoliday = 9



class Store:

    def __init__(self, storeNum):
        self.storeParams = None
        self.departments = [None] * (NUM_DEPTS + 1)
        self.weekFeatureSets = [None] * (NUM_WEEKS_HISTORICAL + 1)
        self.storeNum = storeNum
        self.initialize_depts()

    def initialize_depts(self):
        for deptNum in range(1, NUM_DEPTS + 1):
            self.departments[deptNum] = Dept(deptNum)

    def set_weekly_sales_averages(self, storeDataFrame):
        for deptNum in range(1, NUM_DEPTS + 1):
            # print("Dept: ", deptNum)
            deptDataFrame = storeDataFrame[storeDataFrame["Dept"] == deptNum]
            self.departments[deptNum].set_weekly_sales_averages(deptDataFrame)

    def set_week_feature_sets(self, storeDataFrame):
        for index, record in storeDataFrame.iterrows():
            self.weekFeatureSets[record["AbsoluteWeekNum"]] = record.as_matrix()[3:]

    def get_average_for_future_week(self, futureWeek: FutureWeek) -> float:
        # try:
        return self.departments[futureWeek.deptNum].get_average_for_future_week(futureWeek)
        # except AttributeError:
        #     dum = 4

    def get_average_of_all_depts_for_future_week(self, futureWeek: FutureWeek) -> float:
        deptAverages = []

        for deptNum in DEPTS_RANGE:
            dept = self.departments[deptNum]

            try:
                deptAverages.append(dept.get_average_for_future_week(futureWeek))
            except UnableToCalculateAverageError:
                pass

        averageOverAllDepts = average(deptAverages)

        if math.isnan(averageOverAllDepts):
            raise UnableToCalculateAverageError("No values for Dept-WeekNum doubles of this store")
        else:
            return averageOverAllDepts



class WeekFeatureSet:

    def __init__(self, array):
        self.values = array


class RegressionFit:

    def __init__(self, dataFrame: pd.DataFrame, independentVariable: str):
        self.r2Value = None
        self.slope = None
        self.intercept = None
        self.numDataPoints = None
        self.get_fit_and_set_values(dataFrame, independentVariable)

    def get_fit_and_set_values(self, dataFrame: pd.DataFrame, independentVariable: str):
        independentDataFrame = dataFrame[independentVariable]
        dependetDataFrame = dataFrame.Normalized_Weekly_Sales

        fitResults = numpy.polyfit(numpy.array(independentDataFrame.values, dtype=float), numpy.array(dependetDataFrame.values, dtype=float), 1, full=True)
        model = ols(y=dependetDataFrame, x=independentDataFrame)

        self.slope = fitResults[0][0]
        self.intercept = fitResults[0][1]
        self.r2Value = model.r2
        self.numDataPoints = len(dependetDataFrame)

class RegressionFitsSet:

    def __init__(self):
        self.regressionFits = {}

    def set_regression_fit(self, independentVariable: str, regressionFit: RegressionFit):
        self.regressionFits[independentVariable] = regressionFit

    def get_regression_fit(self, minNumDataPoints: int, r2Thresh: float, independentVarName: str) -> RegressionFit:
        if independentVarName not in self.regressionFits:
            raise UnacceptableFitError("No Fit Available (insufficient samples)")

        if self.regressionFits[independentVarName].numDataPoints < minNumDataPoints:
            raise UnacceptableFitError("Not enough data points for reliable fit")

        if self.regressionFits[independentVarName].r2Value < r2Thresh:
            raise UnacceptableFitError("R2 Value Below Threshold")

        return self.regressionFits[independentVarName]

class Dept:
    def __init__(self, deptNum):
        self.deptNum = deptNum
        self.weekSaleAverages = [None] * (NUM_WEEKS + 1)
        self.deptSalesAverage = 0
        self.deptSalesStd = 0
        self.initialize_week_sale_averages()
        self.regressionFitsSet = RegressionFitsSet()

    def initialize_week_sale_averages(self):
        for weekNum in range(1, NUM_WEEKS + 1):
            self.weekSaleAverages[weekNum] = WeekSaleAverage(weekNum)

    def set_weekly_sales_averages(self, deptDataFrame):
        for weekNum in range(1, NUM_WEEKS + 1):
            weekDataFrame = deptDataFrame[abs(deptDataFrame["WeekNum"] - weekNum) < 2]
            self.weekSaleAverages[weekNum].set_sale_averages(weekDataFrame)

    def set_dept_avg_and_std(self, deptAvg: float, deptStd: float):
        self.deptSalesAverage = deptAvg
        self.deptSalesStd = deptStd

    def get_average_for_future_week(self, futureWeek: FutureWeek) -> float:
        return self.weekSaleAverages[futureWeek.weekNum].get_average_for_future_week(futureWeek)

# weightings = {-2: 10, -1: 20, 0: 40, 1: 20, 2: 10}
weekOffsetWeightings = {-1: 0.5, 0: 1, 1: 0.5}
yearWeightings = {2010: 2, 2011: 10, 2012: 50}

class WeekSaleAverage:
    numDoublesWithLowSampleSize = 0

    def __init__(self, weekNum):
        self.holidayNormalizedSalesAverage = None
        self.nonHolidayNormalizedSalesAverage = None
        self.numHolidayValues = 0
        self.numNonHolidayValues = 0
        self.weekNum = weekNum

    def get_weighted__normalized_sales_value(self, dataFrame):
        weightedSalesProduct = 0
        totalWeighting = 0

        # for relativeIndex in weightings.keys():
        #     averageNormalizedSales = average(dataFrame[dataFrame["WeekNum"] == (self.weekNum + relativeIndex)]["Normalized_Weekly_Sales"])
        #     if not math.isnan(averageNormalizedSales):
        #         weightedSalesProduct += averageNormalizedSales * weightings[relativeIndex]
        #         totalWeighting += weightings[relativeIndex]

        for index, record in dataFrame.iterrows():
            weekOffset = record["WeekNum"] - self.weekNum
            weighting = weekOffsetWeightings[weekOffset] + yearWeightings[record['Year']]

            weightedSalesProduct += record["Normalized_Weekly_Sales"] * weighting
            totalWeighting += weighting
        try:
            return weightedSalesProduct / totalWeighting
        except ZeroDivisionError:
            return float('nan')

    def set_sale_averages(self, weekDataFrame):
        holidaySalesData = weekDataFrame[weekDataFrame["IsHoliday"] == True]
        nonHolidaySalesData = weekDataFrame[weekDataFrame["IsHoliday"] == False]

        self.holidayNormalizedSalesAverage = self.get_weighted__normalized_sales_value(holidaySalesData)
        self.nonHolidayNormalizedSalesAverage = self.get_weighted__normalized_sales_value(nonHolidaySalesData)

        self.numHolidayValues = len(holidaySalesData)
        self.numNonHolidayValues = len(nonHolidaySalesData)

    def get_sales_value_or_raise_error(self, value: float) -> float:
        if math.isnan(value):
            raise UnableToCalculateAverageError("No Average Available for Given Holiday status")
        else:
            return value

    def get_average_for_future_week(self, futureWeek: FutureWeek) -> float:
        if futureWeek.isHoliday:
            return self.get_sales_value_or_raise_error(self.holidayNormalizedSalesAverage)
        else:
            return self.get_sales_value_or_raise_error(self.nonHolidayNormalizedSalesAverage)

class StoreParams:

    def __init__(self, type: str, size: int):
        self.type = type
        self.size = size