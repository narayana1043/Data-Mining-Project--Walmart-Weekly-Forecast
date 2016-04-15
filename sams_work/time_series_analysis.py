import pickle

import numpy

from sales_mapper import *
from sams_work.oop_objects import *
from sams_work.regression import *
from utilities import *

getPickledDataPath = "data/"

def sales_mapping_to_store_objects(trainData: pd.DataFrame, stores: list) -> list:
    # newTrainData["Weekly_Sales_Averaged"] = None

    for storeNum in STORES_RANGE:
        print("Store: ", storeNum)
        storeTrainData = trainData[trainData["Store"] == storeNum]
        stores[storeNum].set_weekly_sales_averages(storeTrainData)

    return stores


def fill_objects_with_historical_features(featuresData: pd.DataFrame, stores: list) -> list:

    for storeNum in STORES_RANGE:
        storeFeaturesData = get_store_rows(featuresData, storeNum)
        stores[storeNum].set_week_feature_sets(storeFeaturesData)

    return stores


def read_pickled_file(fileName):
    with open((SAMS_PICKLED_DATA_PATH + fileName), 'rb') as f:
        return pickle.load(f)


def set_store_params(storesData: pd.DataFrame, stores: list) -> list:

    for index, row in storesData.iterrows():
        stores[row["Store"]].storeParams = StoreParams(row["Type"], row["Size"])

    return stores

def initiliaze_list_of_stores() -> list:
    stores = [None] * (NUM_STORES + 1)

    for storeNum in STORES_RANGE:
        stores[storeNum] = Store(storeNum)

    return stores

def read_store_objects_pickle() -> list:
    return read_pickled_file("store_objects_pickled")

def recreate_stores():
    data = read_pickled_data_from_path(["historical_features", "stores", "train"], SAMS_PICKLED_DATA_PATH)
    featuresData = data["historical_features"]
    storesData = data["stores"]

    trainData = dataFrameGen("train.csv")

    stores = initiliaze_list_of_stores()
    trainData = normalize_department_sales(trainData, stores)

    stores = read_store_objects_pickle()
    stores = sales_mapping_to_store_objects(trainData, stores)
    stores = fill_objects_with_historical_features(featuresData, stores)
    stores = set_store_params(storesData, stores)

    pickle_store_objects(stores)
    data['train'] = trainData

    pickle_data_to_path(SAMS_PICKLED_DATA_PATH, data)


def add_features_and_normalize_train_data(trainData: pd.DataFrame) -> pd.DataFrame:
    stores = read_pickled_file("store_objects_pickled")
    trainData = add_features_to_train_data(stores, trainData)
    trainData = normalize_department_sales(trainData, stores)

    return trainData


data = read_pickled_data_from_path(["test", "stores", "train"], SAMS_PICKLED_DATA_PATH)
testData = data["test"]
trainData = data["train"]
storesData = data["stores"]

# recreate_stores()
# predictionsSet = PredictionsSet(testData)
# pickle_items(predictionsSet, "predictions_set_pickled")


stores = read_store_objects_pickle()

predictionsSet = read_pickled_file("predictions_set_pickled")
predictionsSet.make_predictions(stores)
predictionsSet.write_missing_predictions_to_files()
predictionsSet.write_predictions_to_kaggle_file()