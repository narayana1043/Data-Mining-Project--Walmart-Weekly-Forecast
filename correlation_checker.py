# If you are new to python I just want to show you how we read data in python using pandas.
# I feel it always easy to work with data frames when we have ordered data like in our case.

''' Naming Conventions

Function names should be lowercase, with words separated by underscores as necessary to improve readability.

mixedCase is allowed only in contexts where that's already the prevailing style

Variables = camelCase

'''

import pandas as pd
import re
import os
from datetime import datetime
from sklearn import preprocessing
min_max_scaler = preprocessing.MinMaxScaler()
from matplotlib import pyplot as plt
from scipy.stats import pearsonr
from read_data_functions import *


#Example usage for pickling/unpickling
#pickle_data(read_data())

def normalize():
    #reading pickle data
    data = read_pickled_data()
    train = data['train']
    print(train.head())
    #min max normalization for temperatures
    train['Temperature'] = min_max_scaler.fit_transform(train['Temperature'])
    #min max normalization for sales
    train['Weekly_Sales'] = min_max_scaler.fit_transform(train['Weekly_Sales'])
    for storeNum in range(1,46):
        for deptNum in range(1,100):
            pearsonCorr = abs(pearsonr(train.Weekly_Sales[(train['Dept'] == deptNum) & (train['Store'] == storeNum)],(train.Temperature[(train['Dept'] == deptNum) & (train['Store'] == storeNum)]))[0])
            if pearsonCorr > 0.7:
                print(storeNum,",",deptNum,",",pearsonCorr)

""" *************for ploting correaltion**************************
    for store in range(1,46):
        for dept in range(1,100):
            x = train.Weekly_Sales[(train['Dept'] == dept) & (train['Store'] == store)]
            y = train.Temperature[(train['Dept'] == dept) & (train['Store'] == store)]
            plt.scatter(x,y)
    plt.text(6, 1.5, 'Each data point denotes a department in a store for a particular date', style='italic',fontsize=10,bbox={'facecolor':'grey', 'alpha':0.5, 'pad':10})
    plt.title('Scatter plot to figure out there exists a relation b/w sales and temperatures',fontsize=14)
    plt.xlabel("Weekly Sales")
    plt.ylabel("Temperatures")
    plt.show()
    *******************************************************************"""

normalize()