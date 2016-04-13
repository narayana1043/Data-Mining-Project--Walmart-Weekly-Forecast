

import pandas as pd


def get_dept_rows(dataFrame, deptNum) -> pd.DataFrame:
    return dataFrame[dataFrame["Dept"] == deptNum]


def get_store_rows(dataFrame, storeNum) -> pd.DataFrame:
    return dataFrame[dataFrame["Store"] == storeNum]