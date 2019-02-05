def varmax_model(target_variable, exog_variables, start_date, end_date, plot):
    from statsmodels.tsa.statespace.varmax import VARMAX
    import numpy as np
    
    #Split target variable into training/test set
    train = target_variable[:int(0.7*(len(target_variable)))]
    test = target_variable[int(0.7*(len(target_variable))):]

    exog_variables_train = []
    exog_variables_test = []
    
    #Split external variables into test/training sets
    for variable in exog_variables:
        variable = variable.values
        exog_variables_train.append(variable[:int(0.7*(len(variable)))])
        exog_variables_test.append(variable[int(0.7*(len(variable))):])
        
        
    exog_train = np.column_stack(exog_variables_train)
    exog_test = np.column_stack(exog_variables_test)

    #Fit the model
    y_hat_avg = test
    model = VARMAX(train, exog=exog_train, order=(1, 1)).fit(disp=False)
    # make prediction
    y_hat_avg["VARMAX"] = model.predict(exog=exog_test, start = start_date, end = end_date)
    
    if(plot == True):
        import matplotlib.pyplot as plt
        plt.figure(figsize=(16,8))
        #plt.plot(train[train.columns[0]], label='dod_model.Train')
        plt.plot(test[test.columns[0]], label='Test')
        plt.plot(y_hat_avg['VARMAX'] ,label='VARMAX')
        plt.legend(loc='best')
        plt.show()
        
    print(y_hat_avg)