
import re
import pickle
import pandas as pd
from sales_mapper import dataFrameGen
from constants import *

def get_dept_rows(dataFrame, deptNum) -> pd.DataFrame:
    return dataFrame[dataFrame["Dept"] == deptNum]


def get_store_rows(dataFrame, storeNum) -> pd.DataFrame:
    return dataFrame[dataFrame["Store"] == storeNum]

def add_columns(columns: list, trainData: pd.DataFrame) -> pd.DataFrame:
    for newColName in columns:
        trainData[newColName] = None

    return trainData

def convert_week_num_to_int(dataFrameDict: dict) -> dict:
    for dataFrameName in ["train", "historical_features", "future_features"]:
        for index, record in dataFrameDict[dataFrameName].iterrows():
            dataFrameDict[dataFrameName].set_value(index, "WeekNum", int(record["WeekNum"]))
    return dataFrameDict


def read_data_from_csv_file():
    data = {re.sub(r".csv","",file) : dataFrameGen(file) for file in DATA_FILE_NAMES}
    return data


def pickle_store_objects(stores: list):
    with open((SAMS_PICKLED_DATA_PATH + "store_objects_pickled"), 'wb') as f:
        pickle.dump(stores, f)

def pickle_items(itemsToPickle, pickleFileName):
    with open((SAMS_PICKLED_DATA_PATH + pickleFileName), 'wb') as f:
        pickle.dump(itemsToPickle, f)