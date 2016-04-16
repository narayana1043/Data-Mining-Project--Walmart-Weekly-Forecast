from pandas.stats.api import ols
import statsmodels.api as sm
from sales_mapper import *
from sams_work.oop_objects import *
from utilities import *
from scipy.stats import pearsonr
import numpy

def add_features_to_train_data(stores: list, trainData: pd.DataFrame) -> pd.DataFrame:

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


def normalize_department_sales(trainData: pd.DataFrame, stores: list) -> pd.DataFrame:
    newTrainData = pd.DataFrame(columns=trainData.columns.values)
    newTrainData["Normalized_Weekly_Sales"] = None

    for storeNum in STORES_RANGE:
        print("Store ", storeNum)
        storeDataFrame = get_store_rows(trainData, storeNum)
        for deptNum in DEPTS_RANGE:
            # print("Dept ", deptNum)
            deptDataFrame = get_dept_rows(storeDataFrame, deptNum)
            dataFrameLength = len(deptDataFrame)
            if dataFrameLength == 0:
                continue
            # deptDataFrame['Normalized_Weekly_Sales'] = min_max_scaler.fit_transform(deptDataFrame['Weekly_Sales'].reshape(-1,1))
            deptAverage = average(deptDataFrame['Weekly_Sales'])
            deptStd = deptDataFrame['Weekly_Sales'].std()

            if dataFrameLength == 1 or deptStd == 0:
                deptStd = 0
                deptDataFrame['Normalized_Weekly_Sales'] = 0
            else:
                deptDataFrame['Normalized_Weekly_Sales'] = (deptDataFrame['Weekly_Sales'] - deptAverage) / deptStd

            stores[storeNum].departments[deptNum].set_dept_avg_and_std(deptAverage, deptStd)
            newTrainData = newTrainData.append(deptDataFrame)

    pickle_store_objects(stores)

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

def fill_stores_with_regression_data(trainData: pd.DataFrame, stores: list) -> list:

    goodFitCounts = {'Temperature': 0, 'CPI': 0, 'Fuel_Price': 0, 'Unemployment': 0, 'AbsoluteWeekNum': 0}

    independentVariables = ['Temperature', 'CPI', 'Fuel_Price', 'Unemployment', 'AbsoluteWeekNum']
    for independentVariable in independentVariables:
        for storeNum in STORES_RANGE:
            # print("Store, ", storeNum)
            storeDataFrame = get_store_rows(trainData, storeNum)
            for deptNum in DEPTS_RANGE:
                # print("Dept, ", deptNum)
                deptDataFrame = get_dept_rows(storeDataFrame, deptNum)
                if len(deptDataFrame) > 2:
                    try:
                        regressionFit = RegressionFit(deptDataFrame, independentVariable)
                        stores[storeNum].departments[deptNum].regressionFitsSet.set_regression_fit(independentVariable, regressionFit)
                    except ValueError:
                        print("Value error for regression fit")
    return stores

def print_correlations_all_data(trainData: pd.DataFrame):
    independentColumns = ['Temperature', 'CPI', 'Fuel_Price', 'Unemployment']

    for independentColumn in independentColumns:
        model = ols(y=trainData['Normalized_Weekly_Sales'], x=trainData[independentColumn])
        print(independentColumn + " Correlation: " + str(model.r2))

def print_sales_correlation_vs_absolute_week_num(trainData: pd.DataFrame):

    # storeData = get_store_rows(trainData, 1)

    for deptNum in DEPTS_RANGE:
        deptData = get_dept_rows(trainData, deptNum)
        if len(deptData) == 0:
            continue
        model = ols(y=deptData['Normalized_Weekly_Sales'], x=deptData['CPI'])
        print("Normalized Sales vs. Absolute Week Num Correlation, Dept " + str(deptNum) + ": " + str(model.r2))