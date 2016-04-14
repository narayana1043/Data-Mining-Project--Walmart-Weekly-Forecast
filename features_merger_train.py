from read_data_functions import *

def merger():
    dataFileNames = ["historical_features", "train"]
    data = read_pickled_data(dataFileNames)
    histFeatures = data[dataFileNames[0]]
    train = data[dataFileNames[1]]
    train_features_mixture = pd.concat([train,histFeatures],ignore_index=True)
    #print(train_feature_mixture.head())
    train_features_mixture.to_csv("data/train_features.csv",index=False)
    pickle_data_frame("train_features_mixture",train_features_mixture)


merger()