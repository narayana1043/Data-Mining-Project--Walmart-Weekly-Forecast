from read_data_functions import *
from prettytable import PrettyTable

"""
This code is used to calculate the nulls in the output files produced after prediction.
The calculation of nulls in the hoilday and non holiday are done separately
The second function nulls_counterTable is generates output in a Table that is visually appealing
Libaray used for genrating the table is "prettytable"

"""

def nulls_counter(start,stop):
    for window in range(start,stop):
        for methodType in ["NaiveBayesWindowLT","weightedWindowLT"]:
            dataFrame = get_pickled_data_frame(methodType+str(window))
            isHolidayTrue = dataFrame[dataFrame.IsHoliday == True].Store
            isHolidayTrueWeekly_Sales = dataFrame[dataFrame.IsHoliday == True].Weekly_Sales
            isHolidayFalse = dataFrame[dataFrame.IsHoliday == False].Store
            isHolidayFalseWeekly_Sales = dataFrame[dataFrame.IsHoliday == False].Weekly_Sales
            isHolidayTrueCount = isHolidayTrue.count() - isHolidayTrueWeekly_Sales.count()
            isHolidayFalseCount = isHolidayFalse.count() - isHolidayFalseWeekly_Sales.count()
            print(window,methodType+str(window),isHolidayTrueCount,"  ",isHolidayFalseCount)
            #print(isHolidayTrueCount,",",isHolidayFalseCount)

def nulls_counterTable(start,stop):
    table = PrettyTable(["MethodType","Holiday Nulls","Non-HoliDay Nulls"])
    for window in range(start,stop):
        for methodType in ["NaiveBayesWindowLT","weightedWindowLT"]:
            dataFrame = get_pickled_data_frame(methodType+str(window))
            isHolidayTrue = dataFrame[dataFrame.IsHoliday == True].Store
            isHolidayTrueWeekly_Sales = dataFrame[dataFrame.IsHoliday == True].Weekly_Sales
            isHolidayFalse = dataFrame[dataFrame.IsHoliday == False].Store
            isHolidayFalseWeekly_Sales = dataFrame[dataFrame.IsHoliday == False].Weekly_Sales
            isHolidayTrueCount = isHolidayTrue.count() - isHolidayTrueWeekly_Sales.count()
            isHolidayFalseCount = isHolidayFalse.count() - isHolidayFalseWeekly_Sales.count()
            table.add_row([methodType+str(window),isHolidayTrueCount,isHolidayFalseCount])

    print(table)

nulls_counter(2,8)
nulls_counterTable(2,8)