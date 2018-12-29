import dod_model as m
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import statsmodels.api as sm
from math import sqrt
import numpy as np
import pandas as pd

temp_train_ts = pd.DataFrame(m.train["temp"])
guests_train_ts = pd.DataFrame(m.train["guests"])
severity_train_ts = pd.DataFrame(m.train["severity"])
severity_train_ts = pd.DataFrame(m.train["humidity"])
severity_train_ts = pd.DataFrame(m.train["high_temp"])

temp_test_ts = pd.DataFrame(m.test["temp"])
guests_test_ts = pd.DataFrame(m.test["guests"])
severity_test_ts = pd.DataFrame(m.test["severity"])
severity_test_ts = pd.DataFrame(m.test["humidity"])
severity_test_ts = pd.DataFrame(m.test["high_temp"])


exog_train = np.column_stack((m.train['temp'].values,
                              m.train['severity'].values,
                              m.train['humidity'].values,
                              m.train['high_temp'].values,
                              m.IYK_train['close'].values,
                              m.RHS_train['close'].values,
                              m.FSTA_train['close'].values,
                              m.VDC_train['close'].values,
                              m.PBJ_train['close'].values,
                              m.XLY_train['close'].values,
                              m.FXG_train['close'].values
                              ))

exog_test = np.column_stack((m.test['temp'].values,
                             m.test['severity'].values,
                             m.test['humidity'].values,
                             m.test['high_temp'].values,
                             m.IYK_test['close'].values,
                             m.RHS_test['close'].values,
                             m.FSTA_test['close'].values,
                             m.VDC_test['close'].values,
                             m.PBJ_test['close'].values,
                             m.XLY_test['close'].values,
                             m.FXG_test['close'].values
                             ))

y_hat_avg = m.test.copy()
fit1 = sm.tsa.SARIMAX(guests_train_ts, exog=exog_train, order=(2,0,0), seasonal_order=(1, 1, 1, 12)).fit()
print("SUMMARY: ",fit1.summary())
y_hat_avg['SARIMA'] = fit1.predict(exog=exog_test, start = '2015-03-31', end = '2015-09-30', dynamic=True)
#plt.figure(figsize=(16,8))
#plt.plot( m.train['guests'], label='dod_model.Train')
#plt.plot(m.test['guests'], label='Test')
#plt.plot(y_hat_avg['SARIMA'], label='SARIMA')
#plt.legend(loc='best')
#plt.show()

fit1.plot_diagnostics(figsize=(15, 12))
plt.show()

rms = sqrt(mean_squared_error(m.test.guests, y_hat_avg.SARIMA))
print(rms)