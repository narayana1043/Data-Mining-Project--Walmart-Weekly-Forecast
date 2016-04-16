

#
# def check_num_missing_predictors():
#     stores = read_pickled_file("store_objects_pickled")
#     futureWeeks = read_pickled_file("future_week_objects_pickled")
#
#     missingHolidayPredictions = numpy.full(((NUM_STORES + 1), (NUM_DEPTS + 1), (NUM_WEEKS + 1)), False, dtype=bool)
#     missingNonHolidayPredictions = numpy.full(((NUM_STORES + 1), (NUM_DEPTS + 1), (NUM_WEEKS + 1)), False, dtype=bool)
#
#     for futureWeek in futureWeeks:
#         if futureWeek.isHoliday:
#             try:
#                 if stores[futureWeek.storeNum].departments[futureWeek.deptNum].weekSaleAverages[futureWeek.weekNum].numHolidayValues == 0:
#                     missingHolidayPredictions[futureWeek.storeNum][futureWeek.deptNum][futureWeek.weekNum] = True
#             except AttributeError:
#                 missingHolidayPredictions[futureWeek.storeNum][futureWeek.deptNum][futureWeek.weekNum] = True
#         else:
#             try:
#                 if stores[futureWeek.storeNum].departments[futureWeek.deptNum].weekSaleAverages[futureWeek.weekNum].numNonHolidayValues == 0:
#                     missingNonHolidayPredictions[futureWeek.storeNum][futureWeek.deptNum][futureWeek.weekNum] = True
#             except AttributeError:
#                 missingNonHolidayPredictions[futureWeek.storeNum][futureWeek.deptNum][futureWeek.weekNum] = True
#
#     missingHolidayPredictionsFile = open("missing_holiday_predictions.txt", 'w')
#     missingNonHolidayPredictionsFile = open("missing_non_holiday_predictions.txt", 'w')
#
#     for storeNum in STORES_RANGE:
#         for deptNum in DEPTS_RANGE:
#             for weekNum in WEEKS_RANGE:
#                 if missingNonHolidayPredictions[storeNum][deptNum][weekNum]:
#                     missingNonHolidayPredictionsFile.write(str(storeNum) + "," + str(deptNum) + "," + str(weekNum) + "\n")
#                 if missingHolidayPredictions[storeNum][deptNum][weekNum]:
#                     missingHolidayPredictionsFile.write(str(storeNum) + "," + str(deptNum) + "," + str(weekNum) + "\n")



# def make_predictions_sequential_methods(self, stores: list):
#
#     for futureWeek in self.futureWeeks:
#         futureWeekStore = stores[futureWeek.storeNum]
#         futureWeekDept = futureWeekStore.departments[futureWeek.deptNum]
#         predictedNormalizedSale = 0
#         predictionMethod = ""
#
#         try:
#             predictedNormalizedSale = float('nan')
#             predictedNormalizedSale = futureWeekStore.get_average_for_future_week(futureWeek)
#             predictionMethod = "AAW"  # AAW = Average of Adjacent Weeks (i.e. +/- 2 weeks)
#         except UnableToCalculateAverageError:
#             dummyAssignment = None
#             try:
#                 predictedNormalizedSale = get_average_from_all_stores(stores, futureWeek, checkType=True)
#                 predictionMethod = "AAWAllStoresOfSameType"
#             except UnableToCalculateAverageError:
#                 dummyAssignment = None
#                 try:
#                     predictedNormalizedSale = get_average_from_all_stores(stores, futureWeek, checkType=False)
#                     predictionMethod = "AAWAllStores"
#                 except UnableToCalculateAverageError:
#                     dummyAssignment = None
#                     try:
#                         predictedNormalizedSale = futureWeekStore.get_average_of_all_depts_for_future_week(futureWeek)
#                         predictionMethod = "AAWAllDeptsOfStoreForWeekNum"
#                     except UnableToCalculateAverageError:
#                         print("Error: No Prediction Method for this triplet!!")
#
#         # remove these two lines after rerunning normalization with revised std calc
#         if math.isnan(futureWeekDept.deptSalesStd):
#             futureWeekDept.deptSalesStd = 0
#
#         futureWeek.predictedSales = futureWeekDept.deptSalesAverage + predictedNormalizedSale * futureWeekDept.deptSalesStd
#         futureWeek.predictionMethod = predictionMethod


# def make_predictions_with_weighted_average_of_methods(self, stores: list):
#
#     for futureWeek in self.futureWeeks:
#         futureWeekStore = stores[futureWeek.storeNum]
#         futureWeekDept = futureWeekStore.departments[futureWeek.deptNum]
#         predictedNormalizedSale = 0
#         predictionMethod = "Weightings"
#
#         weightedSalesProductSum = 0
#         weightingsSum = 0
#         weightings = [40, 15, 5, 40]
#
#         try:
#             predictedNormalizedSale = futureWeekStore.get_average_for_future_week(futureWeek)
#             weightedSalesProductSum += predictedNormalizedSale * weightings[0]
#             weightingsSum += weightings[0]
#         except UnableToCalculateAverageError:
#             pass
#         try:
#             predictedNormalizedSale = get_average_from_all_stores(stores, futureWeek, checkType=True)
#             weightedSalesProductSum += predictedNormalizedSale * weightings[1]
#             weightingsSum += weightings[1]
#         except UnableToCalculateAverageError:
#             pass
#         try:
#             predictedNormalizedSale = get_average_from_all_stores(stores, futureWeek, checkType=False)
#             weightedSalesProductSum += predictedNormalizedSale * weightings[2]
#             weightingsSum += weightings[2]
#         except UnableToCalculateAverageError:
#             pass
#         try:
#             predictedNormalizedSale = futureWeekStore.get_average_of_all_depts_for_future_week(futureWeek)
#             weightedSalesProductSum += predictedNormalizedSale * weightings[3]
#             weightingsSum += weightings[3]
#         except UnableToCalculateAverageError:
#             pass
#
#         # remove these two lines after rerunning normalization with revised std calc
#         if math.isnan(futureWeekDept.deptSalesStd):
#             futureWeekDept.deptSalesStd = 0
#
#         predictedNormalizedSale = weightedSalesProductSum / weightingsSum
#
#         futureWeek.predictedSales = futureWeekDept.deptSalesAverage + predictedNormalizedSale * futureWeekDept.deptSalesStd
#         futureWeek.predictionMethod = predictionMethod