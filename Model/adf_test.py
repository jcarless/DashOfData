import dod_model
import pandas
train = dod_model.train
test = dod_model.test

#define function for ADF test
from statsmodels.tsa.stattools import adfuller
def adf_test(timeseries):
   #Perform Dickey-Fuller test:
   print ('Results of Dickey-Fuller Test:')
   dftest = adfuller(timeseries, autolag='AIC')
   dfoutput = pandas.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
   for key,value in dftest[4].items():
      dfoutput['Critical Value (%s)'%key] = value
   print (dfoutput)

# apply adf test on the series
adf_test(train['temp'])
adf_test(train['temp_log_diff'])