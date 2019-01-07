import dod_model as m 
from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from posData_preprocessing import posData
from math import sqrt
import numpy as np

y_hat_avg = m.test.copy()
fit1 = ExponentialSmoothing(np.asarray(m.train['guests']),
                            seasonal_periods=7,
                            trend='add', 
                            seasonal='add',).fit()

y_hat_avg['Holt_Winter'] = fit1.forecast(len(m.test))
plt.figure(figsize=(16,8))
plt.plot( m.train['guests'], label='Train')
plt.plot(m.test['guests'], label='Test')
plt.plot(y_hat_avg['Holt_Winter'], label='Holt_Winter')
plt.legend(loc='best')
plt.show()

rms = sqrt(mean_squared_error(m.test.guests, y_hat_avg.Holt_Winter))
print(rms)