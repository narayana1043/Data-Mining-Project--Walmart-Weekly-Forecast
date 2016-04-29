from sams_work.oop_objects import *
from sams_work.predictions_set_object import *
from sales_mapper import *
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

def add_year_to_train():
    trainData = read_pickled_file("train_with_features_pickled")

    trainData['Year'] = None

    for index,record in trainData.iterrows():
        trainData.set_value(index, 'Year', 2009 + math.ceil(record['AbsoluteWeekNum']/52))

    pickle_items(trainData, "train_with_features_pickled_rev1")

def recreate_stores():
    data = read_pickled_data_from_path(["historical_features", "stores", "train"], SAMS_PICKLED_DATA_PATH)
    featuresData = data["historical_features"]
    storesData = data["stores"]

    trainData = read_pickled_file("train_with_features_pickled_rev1")
    # trainData = dataFrameGen("train.csv")

    stores = initiliaze_list_of_stores()
    trainData = normalize_department_sales(trainData, stores)

    stores = read_store_objects_pickle()
    stores = sales_mapping_to_store_objects(trainData, stores)
    stores = fill_objects_with_historical_features(featuresData, stores)
    stores = set_store_params(storesData, stores)
    stores = fill_stores_with_regression_data(trainData, stores)

    pickle_store_objects(stores)

    data['train'] = trainData
    pickle_data_to_path(SAMS_PICKLED_DATA_PATH, data)


def add_features_and_normalize_train_data(trainData: pd.DataFrame) -> pd.DataFrame:
    stores = read_pickled_file("store_objects_pickled")
    trainData = add_features_to_train_data(stores, trainData)
    trainData = normalize_department_sales(trainData, stores)

    return trainData


#Reading in all of the data provided by walmart
data = read_pickled_data_from_path(["test", "stores", "train", "future_features"], SAMS_PICKLED_DATA_PATH)
testData = data["test"]
trainData = data["train"]
storesData = data["stores"]
futureFeaturesData = data["future_features"]


#This "recreate_stores" performs all of the varous steps for constructing the "store" objects that contain historical
#data If these stores have already been created (and pickled), then only the following line of code (read_pikcled_file) is needed.
# recreate_stores()
historicalStores = read_pickled_file("store_objects_pickled")



#uncomment this set of lines if you want to recreate the future store objects
# futureStoreSet = FutureStoreSet(testData)
# historicalStores = read_pickled_file("store_objects_pickled")
# futureStoreSet.fill_stores_with_features_data(futureFeaturesData)
# pickle_items(futureStoreSet, "future_store_set_pickled")

# uncomment this line if you have already created and pickled the future store objects
futureStoreSet = read_pickled_file("future_store_set_pickled")



# One of these lines should be uncommented to make predictions.
futureStoreSet.make_predictions_with_weighted_average_of_methods(historicalStores)
# futureStoreSet.make_predictions_no_nulls_handling(historicalStores)
# futureStoreSet.make_predictions_sequential_methods(historicalStores)


# Uncomment these lines depending on the output you one (ok to run both if desired).
futureStoreSet.write_missing_predictions_to_files()
futureStoreSet.write_predictions_to_kaggle_file()
