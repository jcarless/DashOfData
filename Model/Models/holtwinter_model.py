#holtwinter_model(
#   target_variable: DataFrame containing a series of the variable to be predicted, 
#    split: numeric training/test split decimal ex 0.7
#   plot: boolean Should a graph of the results be plotted?)

def train_test_split(data, n_test):
	return data[:-n_test], data[-n_test:]

def holtwinter_model(target_variable, n_test, plot):
    from statsmodels.tsa.api import ExponentialSmoothing
    from sklearn.metrics import mean_squared_error
    from math import sqrt
    import numpy as np
    
    #Split target variable into training/test set
    train, test = train_test_split(target_variable, n_test)

    
    y_hat_avg = test.copy()
    #Fit the model    
    fit1 = ExponentialSmoothing(np.asarray(train[train.columns[0]]),
                                seasonal_periods=7,
                                trend='add', 
                                seasonal='add',).fit()
    
    #Create forecast and save to dataframe
    y_hat_avg['Holt_Winter'] = fit1.forecast(len(test))
    
    #Calculate RMS
    rms = sqrt(mean_squared_error(test[test.columns[0]], y_hat_avg.Holt_Winter))
    
    #Plot results
    if(plot == True):
        import matplotlib.pyplot as plt
        plt.figure(figsize=(16,8))
        #plt.plot(train[train.columns[0]], label='dod_model.Train')
        plt.plot(test[test.columns[0]], label='Test')
        plt.plot(y_hat_avg['Holt_Winter'], label='Holt_Winter')
        plt.legend(loc='best')
        plt.show()
    
    return {"rms": rms, "summary": fit1.summary()}