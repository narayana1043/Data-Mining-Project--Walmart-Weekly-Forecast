

import pandas as pd
import re
import os
from datetime import datetime
from scipy import average
from constants import *
import threading


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
        self.departments = [None] * (NUM_DEPTS + 1)
        self.weekFeatureSets = [None] * (NUM_WEEKS_HISTORICAL + 1)
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

    def set_week_feature_sets(self, storeDataFrame):
        for index, record in storeDataFrame.iterrows():
            self.weekFeatureSets[record["AbsoluteWeekNum"]] = record.as_matrix()[3:]


class WeekFeatureSet:

    def __init__(self, array):
        self.values = array


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
        self.numHolidayValues = 0
        self.numNonHolidayValues = 0

    def set_sale_averages(self, weekDataFrame):
        holidaySalesValues = weekDataFrame.loc[weekDataFrame["IsHoliday"] == True]["Weekly_Sales"]
        nonHolidaySalesValues = weekDataFrame.loc[weekDataFrame["IsHoliday"] == False]["Weekly_Sales"]
        self.holidaySalesAverage = average(holidaySalesValues)
        self.nonHolidaySalesAverage = average(nonHolidaySalesValues)
        self.numHolidayValues = len(holidaySalesValues)
        self.numNonHolidayValues = len(nonHolidaySalesValues)