# If you are new to python I just want to show you how we read data in python using pandas.
# I feel it always easy to work with data frames when we have ordered data like in our case.

''' Naming Conventions

Function names should be lowercase, with words separated by underscores as necessary to improve readability.

mixedCase is allowed only in contexts where that's already the prevailing style

Variables = camelCase

'''

from scipy import average
from constants import *
from oop_objects import Store
from read_data_functions import *


def sales_mapping_rev1() -> list:
    testData = get_pickled_data_frame("test")
    trainData = get_pickled_data_frame("train")
    testData["Weekly_Sales"] = None

    newTrainData = pd.DataFrame(columns=trainData.columns.values)
    newTrainData["Weekly_Sales_Averaged"] = None
    stores = [None] * (NUM_STORES + 1)

    for storeNum in range(1, NUM_STORES + 1):
        print("Store: ", storeNum)
        stores[storeNum] = Store(storeNum)
        storeTrainData = trainData[trainData["Store"] == storeNum]
        stores[storeNum].set_weekly_sales_averages(storeTrainData)
        break

sales_mapping_rev1()

