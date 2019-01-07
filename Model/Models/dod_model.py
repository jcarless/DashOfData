import sys
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append("Model/PreProcessing")
from posData_preprocessing import posData
import indicies_preprocessing as ind
from econData_preprocessing import econData
from sarima_model import sarimax_model
from holtwinter_model import holtwinter_model
import matplotlib.pyplot as plt
import pandas as pd

cols = [
        "total_sales",
        "guests",
        "check_count",
        "temp",
        "high_temp",
        "humidity",
        "severity",
        "guests_log",
        "guests_log_diff",
        "temp_log",
        "temp_log_diff"
        ]

start_date = '2014-03-31'
end_date = '2018-6-29'

target_variable = pd.DataFrame(posData["guests"])

train = target_variable[:int(0.7*(len(target_variable)))]
test = target_variable[int(0.7*(len(target_variable))):]

exog_variables = [
          posData['temp'],
          posData['severity'],
          posData['humidity'],
          posData['high_temp'],
          ind.IYK['close'],
          ind.RHS['close'],
          ind.FSTA['close'],
          ind.VDC['close'],
          ind.PBJ['close'],
          ind.XLY['close'],
          ind.FXG['close'],
          econData['gdp']
        ]

plt.figure(figsize=(16,8))
#plt.plot(train[train.columns[0]], label='dod_model.Train')
plt.plot(test[test.columns[0]], label='Test')

sarimax_result = sarimax_model(target_variable, exog_variables, train, test, start_date, end_date)
print("SARIMAX Summary: ", sarimax_result["summary"])
print("SARIMAX RMS: ", sarimax_result["rms"])

holtwinter_result = holtwinter_model(target_variable, train, test)
print("HOLTWINTER Summary: ", holtwinter_result["summary"])
print("HOLTWINTER RMS: ", holtwinter_result["rms"])








plt.legend(loc='best')
plt.show()

#fit1.plot_diagnostics(figsize=(15, 12))
#plt.show()