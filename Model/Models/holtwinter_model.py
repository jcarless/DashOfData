import dod_model
from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import posData_preprocessing
from math import sqrt
import numpy as np

posData = posData_preprocessing.posData

train = dod_model.train
test = dod_model.test

y_hat_avg = test.copy()
fit1 = ExponentialSmoothing(np.asarray(train['guests']),
                            seasonal_periods=7,
                            trend='add', 
                            seasonal='add',).fit()

y_hat_avg['Holt_Winter'] = fit1.forecast(len(test))
plt.figure(figsize=(16,8))
plt.plot( train['guests'], label='Train')
plt.plot(test['guests'], label='Test')
plt.plot(y_hat_avg['Holt_Winter'], label='Holt_Winter')
plt.legend(loc='best')
plt.show()

rms = sqrt(mean_squared_error(test.guests, y_hat_avg.Holt_Winter))
print(rms)