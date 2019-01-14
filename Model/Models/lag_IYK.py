from sklearn import datasets
from sklearn import metrics
from sklearn.ensemble import ExtraTreesClassifier
import indicies_preprocessing as ind
from posData_preprocessing import posData
from econData_preprocessing import econData
#from dod_model import target_variable
from pandas import Series
from matplotlib import pyplot
from statsmodels.graphics.tsaplots import plot_acf
import pandas as pd
import numpy as np

#var = ind.IYK["close"]
#var["date"] = ind.IYK["date"]
# fit an Extra Trees model to the data
#model = ExtraTreesClassifier()
#model.fit(posData["guests"])
# display the relative importance of each attribute
#print(model.feature_importances_)

plot_acf(posData["guests"], lags=30)
pyplot.show()

ind.IYK["stock_lag7"]=ind.IYK.stock.shift(-7)

df2=ind.IYK.iloc[7:-7]

#from sklearn.ensemble import RandomForestRegressor
#
#df = pd.DataFrame()
#df["IYK"] = ind.IYK["close"]
#df["GDP"] = econData["gdp"]
#df["temp"] = posData["temp"]
#df["severity"] = posData["severity"]
#df["FXG"] = ind.FXG['close']
#df["XLY"] = ind.XLY['close']
#df["PBJ"] = ind.PBJ['close']
#df["FSTA"] = ind.FSTA['close']
#df["guests"] = posData['guests']
#df["total_sales"] = posData['total_sales']
#df["humidity"] = posData['humidity']
##df["guests_log"] = posData['guests_log']
##df["guests_log_diff"] = posData['guests_log_diff']
#
#
#df["guests"] = df["guests"].astype(int)
#
#names =  df.columns
#
#data = df.values
#target = df["guests"].values
#
## fit an Extra Trees model to the data
#model = RandomForestRegressor()
#model.fit(data, target)
## display the relative importance of each attribute
##print(model.feature_importances_)
#
#print(sorted(zip(map(lambda x: round(x, 4), model.feature_importances_), names), 
#             reverse=True))
#
##from sklearn.ensemble import RandomForestClassifier
##dataset = datasets.load_iris()
### fit an Extra Trees model to the data
##model = RandomForestClassifier()
##model.fit(dataset.data, dataset.target)
### display the relative importance of each attribute
##print(model.feature_importances_)