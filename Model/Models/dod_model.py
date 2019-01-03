import os, sys
sys.path.append("../PreProcessing")
import posData_preprocessing
import indicies_preprocessing as ind
posData = posData_preprocessing.posData

cols = [
        "total_sales",
        "guests",
        "check_count",
        "temp",
        "high_temp",
        "humidity",
        "severity"
        ]
           
#divide into train and test set
train = posData[:int(0.7*(len(posData)))]
test = posData[int(0.7*(len(posData))):]

IYK_train = ind.IYK[:int(0.7*(len(ind.IYK)))]
IYK_test = ind.IYK[int(0.7*(len(ind.IYK))):]

RHS_train = ind.RHS[:int(0.7*(len(ind.RHS)))]
RHS_test = ind.RHS[int(0.7*(len(ind.RHS))):]

FSTA_train = ind.FSTA[:int(0.7*(len(ind.FSTA)))]
FSTA_test = ind.FSTA[int(0.7*(len(ind.FSTA))):]

VDC_train = ind.VDC[:int(0.7*(len(ind.VDC)))]
VDC_test = ind.VDC[int(0.7*(len(ind.VDC))):]

PBJ_train = ind.PBJ[:int(0.7*(len(ind.PBJ)))]
PBJ_test = ind.PBJ[int(0.7*(len(ind.PBJ))):]

XLY_train = ind.XLY[:int(0.7*(len(ind.XLY)))]
XLY_test = ind.XLY[int(0.7*(len(ind.XLY))):]

FXG_train = ind.FXG[:int(0.7*(len(ind.FXG)))]
FXG_test = ind.FXG[int(0.7*(len(ind.FXG))):]


#train['guests'].plot()
#valid['guests'].plot()
#float(train.total_sales).plot
#print(type(train.total_sales))
#int(round(valid.total_sales)).plot

#train.total_sales.astype("float")

#train.guests.plot()
#valid.guests.plot()

#AUTO ARIMA
#from pmdarima import auto_arima
#import matplotlib.pyplot as plt
#model = auto_arima(train, trace=True, error_action='ignore', suppress_warnings=True)
#model.fit(train)
#
#forecast = model.predict(n_periods=len(valid))
#forecast = pandas.DataFrame(forecast,index = valid.index,columns=['Prediction'])
#
##plot the predictions for validation set
#plt.plot(train, label='Train')
#plt.plot(valid, label='Valid')
#plt.plot(forecast, label='Prediction')
#plt.show()
#
##calculate rmse
#from sklearn.metrics import mean_squared_error
#
#rms = sqrt(mean_squared_error(valid,forecast))
#print(rms)

#Model 1
#dd= np.asarray(train.guests)
#y_hat = valid.copy()
#y_hat['naive'] = dd[len(dd)-1]
#plt.figure(figsize=(12,8))
#plt.plot(train.index, train['guests'], label='Train')
#plt.plot(valid.index,valid['guests'], label='Test')
#plt.plot(y_hat.index,y_hat['naive'], label='Naive Forecast')
#plt.legend(loc='best')
#plt.title("Naive Forecast")
#plt.show()
#
#from sklearn.metrics import mean_squared_error
#from math import sqrt
#rms = sqrt(mean_squared_error(test.guests, y_hat.naive))
#print(rms)


#Model 2
#y_hat_avg = test.copy()
#y_hat_avg['avg_forecast'] = train['guests'].mean()
#plt.figure(figsize=(12,8))
#plt.plot(train['guests'], label='Train')
#plt.plot(test['guests'], label='Test')
#plt.plot(y_hat_avg['avg_forecast'], label='Average Forecast')
#plt.legend(loc='best')
#plt.show()
#
#rms = sqrt(mean_squared_error(test.guests, y_hat_avg.avg_forecast))
#print(rms)

#Model 3
#y_hat_avg = test.copy()
#y_hat_avg['moving_avg_forecast'] = train['guests'].rolling(60).mean().iloc[-1]
#plt.figure(figsize=(16,8))
#plt.plot(train['guests'], label='Train')
#plt.plot(test['guests'], label='Test')
#plt.plot(y_hat_avg['moving_avg_forecast'], label='Moving Average Forecast')
#plt.legend(loc='best')
#plt.show()
#
#rms = sqrt(mean_squared_error(test.guests, y_hat_avg.moving_avg_forecast))
#print(rms)

#Model 4
#from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt
#y_hat_avg = test.copy()
#fit2 = SimpleExpSmoothing(np.asarray(train['guests'])).fit(smoothing_level=0.6,optimized=False)
#y_hat_avg['SES'] = fit2.forecast(len(test))
#plt.figure(figsize=(16,8))
#plt.plot(train['guests'], label='Train')
#plt.plot(test['guests'], label='Test')
#plt.plot(y_hat_avg['SES'], label='SES')
#plt.legend(loc='best')
#plt.show()
#
#rms = sqrt(mean_squared_error(test.guests, y_hat_avg.SES))
#print(rms)

#Model 5
#decompfreq = int(24*60/15*7)
#sm.tsa.seasonal_decompose(train.guests.fillna(0)).plot()
#result = sm.tsa.stattools.adfuller(train.guests)
#plt.show()

#Model 6
#y_hat_avg = test.copy()
#
#fit1 = Holt(np.asarray(train['guests'])).fit(smoothing_level = 0.3,smoothing_slope = 0.1)
#y_hat_avg['Holt_linear'] = fit1.forecast(len(test))
#
#plt.figure(figsize=(16,8))
#plt.plot(train['guests'], label='Train')
#plt.plot(test['guests'], label='Test')
#plt.plot(y_hat_avg['Holt_linear'], label='Holt_linear')
#plt.legend(loc='best')
#plt.show()
#
#rms = sqrt(mean_squared_error(test.guests, y_hat_avg.Holt_linear))
#print(rms)