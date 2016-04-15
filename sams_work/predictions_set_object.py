


import datetime
import math
import pandas as pd
from constants import *
from scipy import average


class UnableToCalculateAverageError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class FutureWeek:

    def __init__(self, testRow):
        self.date = testRow['DateReal']
        self.storeNum = testRow['Store']
        self.deptNum = testRow['Dept']
        self.set_week_num(testRow['WeekNum'])
        self.isHoliday = testRow['IsHoliday']
        self.predictedSales = None
        self.predictionMethod = ""

    def to_string_for_kaggle(self) -> str:
        return str(self.storeNum) + "_" + str(self.deptNum) + "_" + self.get_date_for_kaggle() + "," + str(self.predictedSales)


    def get_date_for_kaggle(self) -> str:
        return datetime.datetime.strptime(self.date, '%m/%d/%Y').strftime("%Y-%m-%d")

    def set_week_num(self, weekNum):
        if weekNum == 0:
            self.weekNum = 1
        else:
            self.weekNum = weekNum



def get_average_from_all_stores(stores: list, futureWeek: FutureWeek, checkType: bool) -> float:
    storeAverages = []

    futureWeekStore = stores[futureWeek.storeNum]

    for storeNum in STORES_RANGE:
        store = stores[storeNum]

        if checkType and store.storeParams.type != futureWeekStore.storeParams.type:
            continue

        try:
            storeAverages.append(store.get_average_for_future_week(futureWeek))
        except Exception:
            pass

    avarageFromStoresOfSameType = average(storeAverages)

    if math.isnan(avarageFromStoresOfSameType):
        raise UnableToCalculateAverageError("No values for Stores-Dept-WeekNum-Triplets of This Type")
    else:
        return avarageFromStoresOfSameType


class PredictionsSet:

    def __init__(self, testData: pd.DataFrame):
        self.futureWeeks = self.get_list_of_future_weeks(testData)

    @staticmethod
    def get_list_of_future_weeks(testData: pd.DataFrame) -> list:
        futureWeeks = [None] * len(testData)

        for index, row in testData.iterrows():
            futureWeeks[index] = FutureWeek(row)

        return futureWeeks

    def make_predictions(self, stores: list):

        for futureWeek in self.futureWeeks:
            futureWeekStore = stores[futureWeek.storeNum]
            futureWeekDept = futureWeekStore.departments[futureWeek.deptNum]
            predictedNormalizedSale = 0
            predictionMethod = ""

            try:
                predictedNormalizedSale = float('nan')
                predictedNormalizedSale = futureWeekStore.get_average_for_future_week(futureWeek)
                predictionMethod = "AAW"  # AAW = Average of Adjacent Weeks (i.e. +/- 2 weeks)
            except UnableToCalculateAverageError:
                try:
                    predictedNormalizedSale = get_average_from_all_stores(stores, futureWeek, checkType=True)
                    predictionMethod = "AAWAllStoresOfSameType"
                except UnableToCalculateAverageError:
                    try:
                        predictedNormalizedSale = get_average_from_all_stores(stores, futureWeek, checkType=False)
                        predictionMethod = "AAWAllStores"
                    except UnableToCalculateAverageError:
                        try:
                            predictedNormalizedSale = futureWeekStore.get_average_of_all_depts_for_future_week(
                                futureWeek)
                            predictionMethod = "AAWAllDeptsOfStoreForWeekNum"
                        except UnableToCalculateAverageError:
                            print("Error: No Prediction Method for this triplet!!")

            # remove these two lines after rerunning normalization with revised std calc
            if math.isnan(futureWeekDept.deptSalesStd):
                futureWeekDept.deptSalesStd = 0

            futureWeek.predictedSales = futureWeekDept.deptSalesAverage + predictedNormalizedSale * futureWeekDept.deptSalesStd
            futureWeek.predictionMethod = predictionMethod

    def write_missing_predictions_to_files(self):

        missingHolidayPredictionsFile = open("missing_holiday_predictions.txt", 'w')
        missingNonHolidayPredictionsFile = open("missing_non_holiday_predictions.txt", 'w')

        missingHolidayPredictionsFile.write("Store, Dept, WeekNum\n")
        missingNonHolidayPredictionsFile.write("Store, Dept, WeekNum\n")

        for futureWeek in self.futureWeeks:

            if math.isnan(futureWeek.predictedSales) or futureWeek.predictedSales == None:
                if futureWeek.isHoliday:
                    missingHolidayPredictionsFile.write(
                        str(futureWeek.storeNum) + "," + str(futureWeek.deptNum) + "," + str(futureWeek.weekNum) + "\n")
                else:
                    missingNonHolidayPredictionsFile.write(
                        str(futureWeek.storeNum) + "," + str(futureWeek.deptNum) + "," + str(futureWeek.weekNum) + "\n")

    def write_predictions_to_kaggle_file(self):
        predictionsFile = open("kaggle_predictions.txt", 'w')

        predictionsFile.write("Id,Weekly_Sales\n")

        for futureWeek in self.futureWeeks:
            predictionsFile.write(futureWeek.to_string_for_kaggle() + "\n")
