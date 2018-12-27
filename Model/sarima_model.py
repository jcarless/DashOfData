from dod_model import test, train
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from posData_preprocessing import posData
import statsmodels.api as sm
from math import sqrt
import numpy as np

y_hat_avg = test.copy()
fit1 = sm.tsa.statespace.SARIMAX(train.guests, order=(2, 1, 4),seasonal_order=(0,1,1,7)).fit()
print("FIT: ", fit1)
y_hat_avg['SARIMA'] = fit1.predict(start="2015-03-09", end="2015-09-30", dynamic=True)
plt.figure(figsize=(16,8))
plt.plot( train['guests'], label='Train')
plt.plot(test['guests'], label='Test')
plt.plot(y_hat_avg['SARIMA'], label='SARIMA')
plt.legend(loc='best')
plt.show()

rms = sqrt(mean_squared_error(test.guests, y_hat_avg.SARIMA))
print(rms)


print(np.asarray(posData))
print(posData.index)

mod_ar2 = sm.tsa.SARIMAX(posData, order=(2,0,0))