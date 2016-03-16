''' Naming Conventions

Function names should be lowercase, with words separated by underscores as necessary to improve readability.

mixedCase is allowed only in contexts where that's already the prevailing style

Use the function naming rules: lowercase with words separated by underscores as necessary to improve readability.

'''

import pandas as pd
import re

#Reading data from files to generate a pandas data frame
def dataFrameGen(fileName):
    dataFrame = pd.read_csv(fileName, header = 0)
    #print(dataFrame.head())
    return dataFrame

#reading the files from locations and making a dictionary of data
def read_data():
    # data file names
    fileNames = ["stores.csv","features.csv","train.csv"]
    #creating a dictionary of data example data[stores] has data of the stores as dataframes defined by pandas
    data = {re.sub(r".csv","",file) : dataFrameGen(file) for file in fileNames}
    #displaying the first five lines of data from every file
    #this is only to cross check that everything works as per thoughts
    for key in data.keys():
        print(data[key].head())


read_data()