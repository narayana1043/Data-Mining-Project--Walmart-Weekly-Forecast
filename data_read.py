''' Naming Conventions

Function names should be lowercase, with words separated by underscores as necessary to improve readability.

mixedCase is allowed only in contexts where that's already the prevailing style

Use the function naming rules: lowercase with words separated by underscores as necessary to improve readability.

'''

import pandas as pd

def data_read(fileName):
    dataFrame = pd.read_csv(fileName, header = 0)
    print(dataFrame.head())

data_read("stores.csv")
