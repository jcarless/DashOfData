#sarimax_model(target_variable: DataFrame containing a series of the variable to be predicted, 
#    exog_variables: List of DataFrames, each containing an external variable series to include in modeling,  
#    start_date: YYYY-M-D Start of date range used to train/test data, 
#    end_date: YYYY-M-D End of date range used to train/test data, 
#    split: numeric training/test split decimal ex 0.7
#    plot: boolean Should a graph of the results be plotted?)

def train_test_split(data, n_test):
	return data[:-n_test], data[-n_test:]

def sarimax_model(target_variable, exog_variables, start_date, end_date, n_test, plot):
    import os, sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from sklearn.metrics import mean_squared_error
    import statsmodels.api as sm
    from math import sqrt
    import numpy as np
    import pandas as pd
    from sarimax_params import get_params
        
#    Split target variable into training/test set
    train, test = train_test_split(target_variable, n_test)
    
    exog_variables_train = []
    exog_variables_test = []
    
    #Split external variables into test/training sets
    for variable in exog_variables:
        variable = variable.values
        var_train, var_test = train_test_split(variable, n_test)
        var_test = pd.DataFrame(var_test)
        var_train = pd.DataFrame(var_train)

        exog_variables_train.append(var_train)
        exog_variables_test.append(var_test)
        
    exog_train = np.column_stack(exog_variables_train)
    exog_test = np.column_stack(exog_variables_test)
    
    #Get best model configuration
    p,d,q,P,D,Q,s = get_params("sarimax", 24, 1)
        
    #Fit the model
    y_hat_avg = test
    fit1 = sm.tsa.SARIMAX(train, 
                          exog=exog_train, 
                          enforce_invertibility = False, 
                          order=(p,d,q), 
                          seasonal_order=(P,D,Q,s)).fit()
    
    #Create prediction and add to dataframe
    y_hat_avg['SARIMA'] = fit1.predict(exog=exog_test, start=start_date, end=end_date, dynamic=False)
    
    
    if(plot == True):
        import matplotlib.pyplot as plt
        plt.figure(figsize=(16,8))
        #plt.plot(train[train.columns[0]], label='dod_model.Train')
        plt.plot(test[test.columns[0]], label='Test')
        plt.plot(y_hat_avg['SARIMA'], label='SARIMA')
        plt.legend(loc='best')
        plt.show()
        
#        #Plot SARMIAX diagnostic
#        fit1.plot_diagnostics(figsize=(15, 12))
#        plt.show()
    
    #Calculate RMS   
    rmse_test = sqrt(mean_squared_error(test[test.columns[0]], y_hat_avg.SARIMA))
#    rmse_train = sqrt(mean_squared_error(train[train.columns[0]], y_hat_avg.SARIMA))
    return { "rmse_test": rmse_test, 
            "rmse_train": "",
            "fit": fit1, 
            "prediction": y_hat_avg['SARIMA'] }