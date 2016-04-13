

from read_data_functions import *
from constants import *
from utilities import *
from oop_objects import *
import statsmodels.api as sm
from pandas.stats.api import ols
import sklearn.linear_model
from sales_mapper import *

getPickledDataPath = "data/"
regressionPickledDataPath = "SamRegression/pickled_data/"


def fill_objects_with_historical_features(stores: list, featuresData: pd.DataFrame) -> list:
    for storeNum in STORES_RANGE:
        storeFeaturesData = get_store_rows(featuresData, storeNum)
        store = Store(storeNum)
        store.set_week_feature_sets(storeFeaturesData)
        stores[storeNum] = store

    return stores

def add_columns(columns: list, trainData: pd.DataFrame) -> pd.DataFrame:
    for newColName in columns:
        trainData[newColName] = None

    return trainData


def add_features_to_train_data(stores: list, trainData) -> pd.DataFrame:

    trainData = add_columns(featureStringToNum.keys(), trainData)
    newTrainData = pd.DataFrame(columns=trainData.columns.values)

    for storeNum in STORES_RANGE:
        print("Store ", storeNum)
        storeDataFrame = get_store_rows(trainData, storeNum)
        weekFeatureSets = stores[storeNum].weekFeatureSets

        for index, record in storeDataFrame.iterrows():

            weekFeatureSet = weekFeatureSets[int(record["AbsoluteWeekNum"])]
            storeDataFrame.set_value(index, "Temperature", weekFeatureSet[Feature.Temperature.value])
            storeDataFrame.set_value(index, "Fuel_Price", weekFeatureSet[Feature.Fuel_Price.value])
            storeDataFrame.set_value(index, "Unemployment", weekFeatureSet[Feature.Unemployment.value])
            storeDataFrame.set_value(index, "CPI", weekFeatureSet[Feature.CPI.value])

        newTrainData = newTrainData.append(storeDataFrame)

    return newTrainData


def normalize_department_sales(trainData: pd.DataFrame) -> pd.DataFrame:
    newTrainData = pd.DataFrame(columns=trainData.columns.values)
    newTrainData["Normalized_Weekly_Sales"] = None

    for storeNum in STORES_RANGE:
        print("Store ", storeNum)
        storeDataFrame = get_store_rows(trainData, storeNum)
        for deptNum in DEPTS_RANGE:
            print("Dept ", deptNum)
            deptDataFrame = get_dept_rows(storeDataFrame, deptNum)
            if len(deptDataFrame) == 0:
                continue
            # deptDataFrame['Normalized_Weekly_Sales'] = min_max_scaler.fit_transform(deptDataFrame['Weekly_Sales'].reshape(-1,1))
            deptDataFrame['Normalized_Weekly_Sales'] = (deptDataFrame['Weekly_Sales'] - average(deptDataFrame['Weekly_Sales']))/deptDataFrame['Weekly_Sales'].std()

            newTrainData = newTrainData.append(deptDataFrame)

    return newTrainData


def get_files_for_printing_correlations() -> dict:
    files = {
        'Temperature': open("r2_values_Temperature.txt", 'w'),
        'CPI': open("r2_values_CPI.txt", 'w'),
        'Fuel_Price': open("r2_values_Fuel_Price.txt", 'w'),
        'Unemployment': open("r2_values_Unemployment.txt", 'w'),
    }
    return files

def calculate_and_print_correlations(trainData: pd.DataFrame):
    files = get_files_for_printing_correlations()
    independentColumns = ['Temperature', 'CPI', 'Fuel_Price', 'Unemployment']
    for independentColumn in independentColumns:
        printedBadSample = False
        printedMedSample = False
        for storeNum in STORES_RANGE:
            storeDataFrame = get_store_rows(trainData, storeNum)
            # storeDataFrame = trainData
            for deptNum in DEPTS_RANGE:
                print("Dept, ", deptNum)
                deptDataFrame = get_dept_rows(storeDataFrame, deptNum)
                # if storeNum == 33 and deptNum == 8 and independentColumn == "Unemployment":
                #     files[independentColumn].write(deptDataFrame.to_string() + "\n")
                if len(deptDataFrame) > 19:
                    model = ols(y=deptDataFrame['Normalized_Weekly_Sales'], x=deptDataFrame[independentColumn])
                    r2Value = model.r2
                    if r2Value > 0.5:
                        files[independentColumn].write("Store, " + str(storeNum) + " Dept, " + str(deptNum) + " Length, " + str(
                            len(deptDataFrame)) + " R2, " + str(r2Value) + "\n")
                    # if r2Value > 0.5 and r2Value < 0.6 and not printedMedSample:
                    #     files[independentColumn].write(
                    #         "Store, " + str(storeNum) + " Dept, " + str(deptNum) + " Length, " + str(
                    #             len(deptDataFrame)) + " R2, " + str(r2Value) + "\n")
    for file in files.items():
        file.close()



data = read_pickled_data_from_path(["train", "stores", "historical_features"], regressionPickledDataPath)
trainData = data["train"]

featuresData = data["historical_features"]
stores = [None] * (NUM_STORES + 1)

stores = sales_mapping_rev1()
stores = fill_objects_with_historical_features(stores, featuresData)
trainData = add_features_to_train_data(stores, trainData)
trainData = normalize_department_sales(trainData)
#
# data["train"] = trainData
# pickle_data(writePickledDataPath, data)

# data = read_pickled_data_from_path(["train", "stores", "historical_features"], writePickledDataPath)
# calculate_and_print_correlations(data['train'])