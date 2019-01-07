import dod_model
import pandas
train = dod_model.train
test = dod_model.test

# define function for kpss test
from statsmodels.tsa.stattools import kpss
#define KPSS
def kpss_test(timeseries):
   print ('Results of KPSS Test:')
   kpsstest = kpss(timeseries, regression='c')
   kpss_output = pandas.Series(kpsstest[0:3], index=['Test Statistic','p-value','Lags Used'])
   
   for key,value in kpsstest[3].items():
       kpss_output['Critical Value (%s)'%key] = value
   print ("OUTPUT: ", kpss_output)
   
kpss_test(train['guests_log'])
print("========")
kpss_test(train['guests'])