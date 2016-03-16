# If you are new to python I just want to show you how we read data in python using pandas.
# I feel it always easy to work with data frames when we have ordered data like in our case.

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
    for key,value in data.items():
        print(key)
        print(value.head(),"\n")


read_data()

'''
train
   Store  Dept        Date  Weekly_Sales IsHoliday
0      1     1  2010-02-05      24924.50     False
1      1     1  2010-02-12      46039.49      True
2      1     1  2010-02-19      41595.55     False
3      1     1  2010-02-26      19403.54     False
4      1     1  2010-03-05      21827.90     False

features
   Store        Date  Temperature  Fuel_Price  MarkDown1  MarkDown2  \
0      1  2010-02-05        42.31       2.572        NaN        NaN
1      1  2010-02-12        38.51       2.548        NaN        NaN
2      1  2010-02-19        39.93       2.514        NaN        NaN
3      1  2010-02-26        46.63       2.561        NaN        NaN
4      1  2010-03-05        46.50       2.625        NaN        NaN

   MarkDown3  MarkDown4  MarkDown5         CPI  Unemployment IsHoliday
0        NaN        NaN        NaN  211.096358         8.106     False
1        NaN        NaN        NaN  211.242170         8.106      True
2        NaN        NaN        NaN  211.289143         8.106     False
3        NaN        NaN        NaN  211.319643         8.106     False
4        NaN        NaN        NaN  211.350143         8.106     False

stores
   Store Type    Size
0      1    A  151315
1      2    A  202307
2      3    B   37392
3      4    A  205863
4      5    B   34875

'''