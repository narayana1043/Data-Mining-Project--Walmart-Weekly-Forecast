from pandas.stats.api import ols

from sales_mapper import *
from sams_work.oop_objects import *
from utilities import *


def add_features_to_train_data(stores: list, trainData) -> pd.DataFrame:

    trainData = add_columns(["Temperature", "Fuel_Price", "Unemployment", "CPI", "IsHoliday"], trainData)
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
            storeDataFrame.set_value(index, "IsHoliday", weekFeatureSet[Feature.IsHoliday.value])

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
        for storeNum in STORES_RANGE:
            storeDataFrame = get_store_rows(trainData, storeNum)
            for deptNum in DEPTS_RANGE:
                print("Dept, ", deptNum)
                deptDataFrame = get_dept_rows(storeDataFrame, deptNum)
                if len(deptDataFrame) > 19:
                    model = ols(y=deptDataFrame['Normalized_Weekly_Sales'], x=deptDataFrame[independentColumn])
                    r2Value = model.r2
                    if r2Value > 0.5:
                        files[independentColumn].write("Store, " + str(storeNum) + " Dept, " + str(deptNum) + " Length, " + str(len(deptDataFrame)) + " R2, " + str(r2Value) + "\n")

