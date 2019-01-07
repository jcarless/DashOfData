from statsmodels.tsa.api import ExponentialSmoothing
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from math import sqrt
import numpy as np

def holtwinter_model(target_variable, train, test):

    y_hat_avg = test
    fit1 = ExponentialSmoothing(np.asarray(train[train.columns[0]]),
                                seasonal_periods=7,
                                trend='add', 
                                seasonal='add',).fit()
    
    y_hat_avg['Holt_Winter'] = fit1.forecast(len(test))
    plt.plot(y_hat_avg['Holt_Winter'], label='Holt_Winter')
    rms = sqrt(mean_squared_error(test[test.columns[0]], y_hat_avg.Holt_Winter))
    
    return {"rms": rms, "summary": fit1.summary()}