import pandas
from statsmodels.graphics.tsaplots import plot_acf
from matplotlib import pyplot


# define function for kpss test
from statsmodels.tsa.stattools import kpss
#define KPSS
def kpss_test(timeseries):
   print ('Results of KPSS Test:')
   kpsstest = kpss(timeseries, regression='c')
   kpss_output = pandas.Series(kpsstest[0:3], index=['Test Statistic','p-value','Lags Used'])
   
   for key,value in kpsstest[3].items():
       kpss_output['Critical Value (%s)'%key] = value
       
   plot_acf(timeseries, lags=30)
   pyplot.show()
       
   return kpss_output
#   print ("OUTPUT: ", kpss_output)
   
#kpss_test(train['guests_log'])
#print("========")
#kpss_test(train['guests'])