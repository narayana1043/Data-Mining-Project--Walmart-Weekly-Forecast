

import pandas as pd
import re
import os
from datetime import datetime
from scipy import average
from constants import *
import threading
import math
import pickle
from sams_work.predictions_set_object import *

from enum import Enum

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
        return self.departments[futureWeek.deptNum].get_average_for_future_week(futureWeek)

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


class Dept:
    def __init__(self, deptNum):
        self.deptNum = deptNum
        self.weekSaleAverages = [None] * (NUM_WEEKS + 1)
        self.initialize_week_sale_averages()
        self.deptSalesAverage = 0
        self.deptSalesStd = 0

    def initialize_week_sale_averages(self):
        for weekNum in range(1, NUM_WEEKS + 1):
            self.weekSaleAverages[weekNum] = WeekSaleAverage(weekNum)

    def set_weekly_sales_averages(self, deptDataFrame):
        for weekNum in range(1, NUM_WEEKS + 1):
            weekDataFrame = deptDataFrame[abs(deptDataFrame["WeekNum"] - weekNum) < 3]
            self.weekSaleAverages[weekNum].set_sale_averages(weekDataFrame)

    def set_dept_avg_and_std(self, deptAvg: float, deptStd: float):
        self.deptSalesAverage = deptAvg
        self.deptSalesStd = deptStd

    def get_average_for_future_week(self, futureWeek: FutureWeek) -> float:
        return self.weekSaleAverages[futureWeek.weekNum].get_average_for_future_week(futureWeek)

weightings = {-2: 10, -1: 20, 0: 40, 1: 20, 2: 10}


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

        for relativeIndex in weightings.keys():
            averageNormalizedSales = average(dataFrame[dataFrame["WeekNum"] == (self.weekNum + relativeIndex)]["Normalized_Weekly_Sales"])
            if not math.isnan(averageNormalizedSales):
                weightedSalesProduct += averageNormalizedSales * weightings[relativeIndex]
                totalWeighting += weightings[relativeIndex]
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

    def get_sales_value_or_raise_error(self, value):
        if math.isnan(value):
            raise UnableToCalculateAverageError("No Average Available for Given Holiday status")
        else:
            return value

    def get_average_for_future_week(self, futureWeek: FutureWeek) -> float:
        if futureWeek.isHoliday:
            return self.get_sales_value_or_raise_error(self.holidayNormalizedSalesAverage)
        else:
            return self.get_sales_value_or_raise_error(self.nonHolidayNormalizedSalesAverage)

#
# class StoreSet:
#     def __init__(self):
#         self.stores = [None] * (NUM_STORES + 1)
#
#     def pickle(self):
#         with open((SAMS_PICKLED_DATA_PATH + "store_set_pickled"), 'wb') as f:
#             pickle.dump(self, f)
#
#     def set_store(self, storeNum: int, store: Store):
#         self.stores[storeNum] = store

class StoreParams:

    def __init__(self, type: str, size: int):
        self.type = type
        self.size = size