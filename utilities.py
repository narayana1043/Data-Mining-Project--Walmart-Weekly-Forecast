

import pandas as pd
from sales_mapper import dataFrameGen


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

def read_data_from_file():
    data = {re.sub(r".csv","",file) : dataFrameGen(file) for file in dataFileNames}
    return data