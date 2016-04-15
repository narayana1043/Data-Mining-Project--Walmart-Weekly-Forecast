

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
