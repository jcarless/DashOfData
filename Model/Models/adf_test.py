def adf_test(timeseries):
    import pandas as pd
    from statsmodels.tsa.stattools import adfuller
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
      dfoutput['Critical Value (%s)'%key] = value
      
    return dfoutput