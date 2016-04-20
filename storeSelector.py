from read_data_functions import *
from statistics import mean,stdev

"""
This file contains the functions that figure out which stores perfrom similar to the given store
"""
def closer_stores(nullStore):
    storeData = get_pickled_data_frame("stores")
    returnList = []
    storeNum = nullStore
    storeType = None
    storeSize = None
    for index,store in storeData.iterrows():
        if store["Store"] == storeNum:
            storeType = store["Type"]
            storeSize = store["Size"]
    storeTypeSel = storeData.loc[storeData["Type"] == storeType]
    storeTypeSel.Size = storeTypeSel.Size - storeSize
    storeTypeSel["Size"] = storeTypeSel.loc[:,"Size"].abs()
    storeTypeSel = storeTypeSel.sort_values(["Size"],ascending= [True])
    for index,store in storeTypeSel.iterrows():
       returnList.append(store["Store"])

    return returnList[2:6]

def store_sales_cal(store,dept):
    trainData = get_pickled_data_frame("train")
    filter = trainData[(trainData["Store"]==store) & (trainData["Dept"]== dept)]
    if len(filter.index) < 2:
        return None,None,None
    return {"sum":filter.Weekly_Sales.sum(),"mean":mean(filter.Weekly_Sales),"stdev":stdev(filter.Weekly_Sales)}

def store_features():
    storeFeatures = pd.DataFrame(columns=["Store","Dept","Sales","Sales_Mean","Sales_Stdev"])
    for store in range(1,46):
        print(store)
        for dept in range(1,100):
            storeSalesCal = store_sales_cal(store,dept)
            storeFeatures = storeFeatures.append({"Store":store,"Dept":dept,"Sales":storeSalesCal["sum"],"Sales_Mean":storeSalesCal["mean"],"Sales_Stdev":storeSalesCal["stdev"]},ignore_index=True)
            print(storeFeatures.head())
    pickle_data_frame("stores_features",storeFeatures)
    storeFeatures.to_csv("data/store_features",index=False)

def store_selector(store,dept):
    currStoreSalesCal = store_sales_cal(store,dept)
    storeFeatures = get_pickled_data_frame("stores_features")
    print(storeFeatures)
    storeFeatures["Sales_Mean"] = storeFeatures["Sales_Mean"] - currStoreSalesCal["mean"]
    storeFeatures["Sales_Mean"] = storeFeatures.loc[:,"Sales_Mean"].abs()
    storeFeatures = storeFeatures.sort_values(["Sales_Mean"],ascending=[True])
    storeFeatures = storeFeatures.drop([0])
    storeFeatures = storeFeatures.drop(list(range(6,len(storeFeatures.index)+1)))
    print(storeFeatures.head())
    storeFeatures["Sales_Stdev"] = storeFeatures["Sales_Stdev"] - currStoreSalesCal["stdev"]
    storeFeatures["Sales_Stdev"] = storeFeatures.loc[:,"Sales_Stdev"].abs()
    storeFeatures = storeFeatures.sort_values(["Sales_Stdev"],ascending=[True])
    print(storeFeatures.head())
    #storeFeatures = storeFeatures.reindex()
    print(storeFeatures.head())
    return {"store":storeFeatures.Store.iloc[0], "dept":storeFeatures.Dept.iloc[0]}


#print(closer_stores(1))
#print(store_sales_cal(1,47))
#print(store_features())
#print(store_selector(1,1))
