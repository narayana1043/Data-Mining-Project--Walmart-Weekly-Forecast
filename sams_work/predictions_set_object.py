


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

class UnacceptableFitError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class NoFeatureValueAvailableError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)



class FutureWeekFeatureSet:
    featureNamesList = ['Temperature', 'CPI', 'Fuel_Price', 'Unemployment', 'AbsoluteWeekNum', 'IsHoliday']

    def __init__(self, testRow: pd.DataFrame):
        self.features = {}
        self.set_features(testRow)

    def set_features(self, testRow: pd.DataFrame):
        for featureName in self.featureNamesList:
            featureValue = testRow[featureName]

            if not math.isnan(featureValue):
                self.features[featureName] = featureValue

    def get_feature_value(self, featureName: str):
        return self.features[featureName]


class FutureWeek:

    def __init__(self, testRow: pd.DataFrame):
        self.weekNum = None
        self.absoluteWeekNum = None
        self.date = None
        self.storeNum = None
        self.deptNum = None
        self.predictedSales = None
        self.isHoliday = None
        self.predictionMethod = ""

        self.fill_with_test_data(testRow)

    def fill_with_test_data(self, testRow: pd.DataFrame):
        self.date = testRow['DateReal'].iloc[0]
        self.storeNum = testRow['Store'].iloc[0]
        self.deptNum = testRow['Dept'].iloc[0]
        self.absoluteWeekNum = testRow['AbsoluteWeekNum'].iloc[0]
        self.isHoliday = testRow['IsHoliday'].iloc[0]

        self.set_week_num(testRow['WeekNum'].iloc[0])


    def to_string_for_kaggle(self) -> str:
        return str(self.storeNum) + "_" + str(self.deptNum) + "_" + self.get_date_for_kaggle() + "," + str(self.predictedSales)

    def get_date_for_kaggle(self) -> str:
        return datetime.datetime.strptime(self.date, '%m/%d/%Y').strftime("%Y-%m-%d")

    def set_week_num(self, weekNum):
        if weekNum == 0:
            self.weekNum = 1
        else:
            self.weekNum = weekNum



class FutureDept:
    def __init__(self, deptNum):
        self.deptNum = deptNum
        self.futureWeeks = [None] * (FUTURE_WEEK_MAX + 1)
        self.deptSalesAverage = 0
        self.deptSalesStd = 0
        # self.initialize_future_weeks()

    # def initialize_future_weeks(self):
    #     for weekNum in WEEKS_RANGE_FUTURE:
    #         self.futureWeeks[weekNum] = FutureWeek(weekNum)

    def fill_with_test_data(self, deptTestData: pd.DataFrame):
        for weekNum in WEEKS_RANGE_FUTURE:
            weekTestData = deptTestData[deptTestData["AbsoluteWeekNum"] == weekNum]
            if len(weekTestData) == 0:
                continue

            self.futureWeeks[weekNum] = FutureWeek(weekTestData)


class FutureStore:

    def __init__(self, storeNum):
        self.departments = [None] * (NUM_DEPTS + 1)
        self.weekFeatureSets = [None] * (FUTURE_WEEK_MAX + 1)
        self.storeNum = storeNum
        self.initialize_depts()

    def initialize_depts(self):
        for deptNum in range(1, NUM_DEPTS + 1):
            self.departments[deptNum] = FutureDept(deptNum)

    def set_features(self, storeDataFrame: pd.DataFrame):
        for index, testRow in storeDataFrame.iterrows():
            try:
                self.weekFeatureSets[testRow["AbsoluteWeekNum"]] = FutureWeekFeatureSet(testRow)
            except IndexError:
                dummyAss = 0
    def fill_with_test_data(self, storeTestData: pd.DataFrame):
        for deptNum in DEPTS_RANGE:
            deptDataFrame = storeTestData[storeTestData["Dept"] == deptNum]
            self.departments[deptNum].fill_with_test_data(deptDataFrame)

    def get_feature_value(self, absoluteWeekNum: int, featureName: str):
        if featureName in self.weekFeatureSets[absoluteWeekNum].features:
            return self.weekFeatureSets[absoluteWeekNum].features[featureName]
        else:
            raise NoFeatureValueAvailableError("")

def get_average_from_all_stores(historicalStores: list, futureWeek: FutureWeek, checkType: bool) -> float:
    storeAverages = []

    historicalStore = historicalStores[futureWeek.storeNum]

    for storeNum in STORES_RANGE:
        compareStore = historicalStores[storeNum]

        if checkType and compareStore.storeParams.type != historicalStore.storeParams.type:
            continue

        try:
            storeAverages.append(compareStore.get_average_for_future_week(futureWeek))
        except UnableToCalculateAverageError:
            pass

    avarageFromStoresOfSameType = average(storeAverages)

    if math.isnan(avarageFromStoresOfSameType):
        raise UnableToCalculateAverageError("No values for Stores-Dept-WeekNum-Triplets of This Type")
    else:
        return avarageFromStoresOfSameType


class FutureStoreSet:

    def __init__(self, testData: pd.DataFrame):
        self.futureStores = [None] * (NUM_STORES + 1)
        self.fill_with_test_data(testData)

    def fill_stores_with_features_data(self, futureFeaturesData: pd.DataFrame):

        for storeNum in STORES_RANGE:
            print("Store, " + str(storeNum))
            storeData = futureFeaturesData[futureFeaturesData['Store'] == storeNum]
            self.futureStores[storeNum].set_features(storeData)

    def fill_with_test_data(self, testData: pd.DataFrame):
        for storeNum in STORES_RANGE:
            print("Store, " + str(storeNum))
            storeData = testData[testData['Store'] == storeNum]
            self.futureStores[storeNum] = FutureStore(storeNum)
            self.futureStores[storeNum].fill_with_test_data(storeData)

    def make_predictions_sequential_methods(self, historicalStores: list):

        for storeNum in STORES_RANGE:
            historicalStore = historicalStores[storeNum]
            futureStore = self.futureStores[storeNum]

            for deptNum in DEPTS_RANGE:
                historicalDept = historicalStore.departments[deptNum]
                futureDept = futureStore.departments[deptNum]

                for futureAbsWeekNum in WEEKS_RANGE_FUTURE:
                    futureWeek = futureDept.futureWeeks[futureAbsWeekNum]

                    if futureWeek == None:
                        continue



                    predictedNormalizedSale = 0
                    predictionMethod = ""

                    try:
                        predictedNormalizedSale = float('nan')
                        predictedNormalizedSale = historicalStore.get_average_for_future_week(futureWeek)
                        predictionMethod = "AAW"  # AAW = Average of Adjacent Weeks (i.e. +/- 2 weeks)
                    except UnableToCalculateAverageError:
                        dummyAssignment = None
                        try:
                            predictedNormalizedSale = get_average_from_all_stores(historicalStores, futureWeek, checkType=True)
                            predictionMethod = "AAWAllStoresOfSameType"
                        except UnableToCalculateAverageError:
                            dummyAssignment = None
                            try:
                                predictedNormalizedSale = get_average_from_all_stores(historicalStores, futureWeek, checkType=False)
                                predictionMethod = "AAWAllStores"
                            except UnableToCalculateAverageError:
                                dummyAssignment = None
                                try:
                                    predictedNormalizedSale = historicalStore.get_average_of_all_depts_for_future_week(
                                        futureWeek)
                                    predictionMethod = "AAWAllDeptsOfStoreForWeekNum"
                                except UnableToCalculateAverageError:
                                    print("Error: No Prediction Method for this triplet!!")

                    # remove these two lines after rerunning normalization with revised std calc
                    if math.isnan(historicalDept.deptSalesStd):
                        historicalDept.deptSalesStd = 0

                    futureWeek.predictedSales = historicalDept.deptSalesAverage + predictedNormalizedSale * historicalDept.deptSalesStd
                    futureWeek.predictionMethod = predictionMethod





    def make_predictions_with_weighted_average_of_methods(self, stores: list):
        predictionMethod = "Weightings"
        methodAveragesWeightings = [50, 1, 1, 1]
        R2_THRESH = 0.5
        MIN_NUM_DATA_POINTS = 40
        MAX_REGRESSION_WEIGHT = 10

        for storeNum in STORES_RANGE:
            print("Store, " + str(storeNum))
            historicalStore = stores[storeNum]
            futureStore = self.futureStores[storeNum]

            for deptNum in DEPTS_RANGE:
                historicalDept = historicalStore.departments[deptNum]
                futureDept = futureStore.departments[deptNum]

                for futureAbsWeekNum in WEEKS_RANGE_FUTURE:
                    futureWeek = futureDept.futureWeeks[futureAbsWeekNum]

                    if futureWeek == None:
                        continue

                    weightedSalesProductSum = 0
                    weightingsSum = 0

                    try:
                        predictedNormalizedSale = historicalStore.get_average_for_future_week(futureWeek)
                        weightedSalesProductSum += predictedNormalizedSale * methodAveragesWeightings[0]
                        weightingsSum += methodAveragesWeightings[0]
                    except UnableToCalculateAverageError:
                        pass
                    try:
                        predictedNormalizedSale = get_average_from_all_stores(stores, futureWeek, checkType=True)
                        weightedSalesProductSum += predictedNormalizedSale * methodAveragesWeightings[1]
                        weightingsSum += methodAveragesWeightings[1]
                    except UnableToCalculateAverageError:
                        pass
                    try:
                        predictedNormalizedSale = get_average_from_all_stores(stores, futureWeek, checkType=False)
                        weightedSalesProductSum += predictedNormalizedSale * methodAveragesWeightings[2]
                        weightingsSum += methodAveragesWeightings[2]
                    except UnableToCalculateAverageError:
                        pass
                    try:
                        predictedNormalizedSale = historicalStore.get_average_of_all_depts_for_future_week(futureWeek)
                        weightedSalesProductSum += predictedNormalizedSale * methodAveragesWeightings[3]
                        weightingsSum += methodAveragesWeightings[3]
                    except UnableToCalculateAverageError:
                        pass

                    for independentVarName in historicalDept.regressionFitsSet.regressionFits:
                        try:
                            regressionFit = historicalDept.regressionFitsSet.get_regression_fit(MIN_NUM_DATA_POINTS, R2_THRESH, independentVarName)
                            regressionFitWeight = regressionFit.r2Value * MAX_REGRESSION_WEIGHT
                            futureWeekFeatureValue = futureStore.get_feature_value(futureWeek.absoluteWeekNum, independentVarName)
                            weightedSalesProductSum = (futureWeekFeatureValue * regressionFit.slope + regressionFit.intercept) * regressionFitWeight
                            # weightedSalesProductSum = (futureStore.weekFeatureSets[futureWeek.absoluteWeekNum].features[independentVarName] * regressionFit.slope + regressionFit.intercept) * regressionFitWeight

                            if math.isnan(weightedSalesProductSum):
                                b = 5
                            weightingsSum += regressionFitWeight
                        except (UnacceptableFitError, NoFeatureValueAvailableError):
                            pass

                    # remove these two lines after rerunning normalization with revised std calc
                    if math.isnan(historicalDept.deptSalesStd):
                        historicalDept.deptSalesStd = 0

                    predictedNormalizedSale = weightedSalesProductSum / weightingsSum

                    futureWeek.predictedSales = historicalDept.deptSalesAverage + predictedNormalizedSale * historicalDept.deptSalesStd

                    if math.isnan(futureWeek.predictedSales):
                        b = 5

                    futureWeek.predictionMethod = predictionMethod

    def write_missing_predictions_to_files(self):

        missingHolidayPredictionsFile = open("missing_holiday_predictions.txt", 'w')
        missingNonHolidayPredictionsFile = open("missing_non_holiday_predictions.txt", 'w')

        missingHolidayPredictionsFile.write("Store, Dept, WeekNum\n")
        missingNonHolidayPredictionsFile.write("Store, Dept, WeekNum\n")

        for storeNum in STORES_RANGE:
            print("Store, " + str(storeNum))
            futureStore = self.futureStores[storeNum]

            for deptNum in DEPTS_RANGE:
                futureDept = futureStore.departments[deptNum]

                for futureAbsWeekNum in WEEKS_RANGE_FUTURE:
                    futureWeek = futureDept.futureWeeks[futureAbsWeekNum]

                    if futureWeek == None:
                        continue

                    if math.isnan(futureWeek.predictedSales) or futureWeek.predictedSales == None:
                        if futureWeek.isHoliday:
                            missingHolidayPredictionsFile.write(
                                str(futureWeek.storeNum) + "," + str(futureWeek.deptNum) + "," + str(
                                    futureWeek.weekNum) + "\n")
                        else:
                            missingNonHolidayPredictionsFile.write(
                                str(futureWeek.storeNum) + "," + str(futureWeek.deptNum) + "," + str(
                                    futureWeek.weekNum) + "\n")

    def write_predictions_to_kaggle_file(self):
        predictionsFile = open("kaggle_predictions.txt", 'w')

        predictionsFile.write("Id,Weekly_Sales\n")

        for storeNum in STORES_RANGE:
            print("Store, " + str(storeNum))
            futureStore = self.futureStores[storeNum]

            for deptNum in DEPTS_RANGE:
                futureDept = futureStore.departments[deptNum]

                for futureAbsWeekNum in WEEKS_RANGE_FUTURE:
                    futureWeek = futureDept.futureWeeks[futureAbsWeekNum]

                    if futureWeek == None:
                        continue

                    predictionsFile.write(futureWeek.to_string_for_kaggle() + "\n")
