def kpss_test(timeseries, plot):
    import pandas as pd
    from statsmodels.graphics.tsaplots import plot_acf
    from statsmodels.tsa.stattools import kpss
    
    kpsstest = kpss(timeseries, regression='c')
    kpss_output = pd.Series(kpsstest[0:3], index=['Test Statistic','p-value','Lags Used'])
       
    for key,value in kpsstest[3].items():
        kpss_output['Critical Value (%s)'%key] = value
       
    if plot == True:
        from matplotlib import pyplot
        plot_acf(timeseries, lags=30)
        pyplot.show()
       
    return kpss_output