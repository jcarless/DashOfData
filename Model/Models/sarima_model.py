from sklearn.metrics import mean_squared_error
import statsmodels.api as sm
import matplotlib.pyplot as plt
from math import sqrt
import numpy as np

def sarimax_model(target_variable, exog_variables, train, test, start_date, end_date):
    
    train = target_variable[:int(0.7*(len(target_variable)))]
    test = target_variable[int(0.7*(len(target_variable))):]
        
    exog_variables_train = []
    exog_variables_test = []
    
    for variable in exog_variables:
        variable = variable.values
        exog_variables_train.append(variable[:int(0.7*(len(variable)))])
        exog_variables_test.append(variable[int(0.7*(len(variable))):])
        
    exog_train = np.column_stack(exog_variables_train)
    exog_test = np.column_stack(exog_variables_test)

    y_hat_avg = test
    fit1 = sm.tsa.SARIMAX(train, exog=exog_train, order=(2,0,0), seasonal_order=(1, 1, 1, 12)).fit()
    y_hat_avg['SARIMA'] = fit1.predict(exog=exog_test, start = start_date, end = end_date, dynamic=True)
    plt.plot(y_hat_avg['SARIMA'] ,label='SARIMA')

#    fit1.plot_diagnostics(figsize=(15, 12))
#    plt.show()
    
    rms = sqrt(mean_squared_error(test[test.columns[0]], y_hat_avg.SARIMA))
    return { "rms": rms, "summary": fit1.summary(), "prediction": y_hat_avg['SARIMA'] }