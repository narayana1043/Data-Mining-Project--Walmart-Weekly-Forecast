import pickle

import numpy

from sales_mapper import *
from sams_work.oop_objects import *
from sams_work.regression import *
from utilities import *

getPickledDataPath = "data/"

def sales_mapping_to_store_objects() -> list:
    data = read_pickled_data_from_path(["train"], SAMS_PICKLED_DATA_PATH)
    trainData = data["train"]

    newTrainData = pd.DataFrame(columns=trainData.columns.values)
    newTrainData["Weekly_Sales_Averaged"] = None
    stores = [None] * (NUM_STORES + 1)

    for storeNum in STORES_RANGE:
        print("Store: ", storeNum)
        stores[storeNum] = Store(storeNum)
        storeTrainData = trainData[trainData["Store"] == storeNum]
        stores[storeNum].set_weekly_sales_averages(storeTrainData)

    return stores

def fill_objects_with_historical_features(stores: list, featuresData: pd.DataFrame) -> list:

    for storeNum in STORES_RANGE:
        storeFeaturesData = get_store_rows(featuresData, storeNum)
        stores[storeNum].set_week_feature_sets(storeFeaturesData)

    return stores

def get_list_of_future_weeks(testData) -> list:
    futureWeeks = [None] * len(testData)

    for index, row in testData.iterrows():
        futureWeeks[index] = FutureWeek(row)

    return futureWeeks

def read_pickled_file(fileName):
    with open((SAMS_PICKLED_DATA_PATH + fileName), 'rb') as f:
        return pickle.load(f)

def check_num_missing_predictors():
    stores = read_pickled_file("store_objects_pickled")
    futureWeeks = read_pickled_file("future_week_objects_pickled")

    missingHolidayPredictions = numpy.full(((NUM_STORES + 1), (NUM_DEPTS + 1), (NUM_WEEKS + 1)), False, dtype=bool)
    missingNonHolidayPredictions = numpy.full(((NUM_STORES + 1), (NUM_DEPTS + 1), (NUM_WEEKS + 1)), False, dtype=bool)

    for futureWeek in futureWeeks:
        if futureWeek.isHoliday:
            try:
                if stores[futureWeek.storeNum].departments[futureWeek.deptNum].weekSaleAverages[futureWeek.weekNum].numHolidayValues == 0:
                    missingHolidayPredictions[futureWeek.storeNum][futureWeek.deptNum][futureWeek.weekNum] = True
            except AttributeError:
                missingHolidayPredictions[futureWeek.storeNum][futureWeek.deptNum][futureWeek.weekNum] = True
        else:
            try:
                if stores[futureWeek.storeNum].departments[futureWeek.deptNum].weekSaleAverages[futureWeek.weekNum].numNonHolidayValues == 0:
                    missingNonHolidayPredictions[futureWeek.storeNum][futureWeek.deptNum][futureWeek.weekNum] = True
            except AttributeError:
                missingNonHolidayPredictions[futureWeek.storeNum][futureWeek.deptNum][futureWeek.weekNum] = True

    missingHolidayPredictionsFile = open("missing_holiday_predictions.txt", 'w')
    missingNonHolidayPredictionsFile = open("missing_non_holiday_predictions.txt", 'w')

    for storeNum in range(1, NUM_STORES):#STORES_RANGE
        for deptNum in DEPTS_RANGE:
            for weekNum in WEEKS_RANGE:
                if missingNonHolidayPredictions[storeNum][deptNum][weekNum]:
                    missingNonHolidayPredictionsFile.write(str(storeNum) + "," + str(deptNum) + "," + str(weekNum) + "\n")
                if missingHolidayPredictions[storeNum][deptNum][weekNum]:
                    missingHolidayPredictionsFile.write(str(storeNum) + "," + str(deptNum) + "," + str(weekNum) + "\n")


def recreate_stores():
    data = read_pickled_data_from_path(["historical_features"], SAMS_PICKLED_DATA_PATH)
    featuresData = data["historical_features"]

    stores = sales_mapping_to_store_objects()
    stores = fill_objects_with_historical_features(stores, featuresData)

    with open((SAMS_PICKLED_DATA_PATH + "store_objects_pickled"), 'wb') as f:
        pickle.dump(stores, f)


def add_features_and_normalize_train_data(trainData: pd.DataFrame) -> pd.DataFrame:
    stores = read_pickled_file("store_objects_pickled")
    trainData = add_features_to_train_data(stores, trainData)
    trainData = normalize_department_sales(trainData)

    return trainData


check_num_missing_predictors()
