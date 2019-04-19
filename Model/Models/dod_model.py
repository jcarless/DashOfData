import os
import sys
sys.path.append("Model/PreProcessing")
sys.path.append("Model/Models")
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(
        "/Users/jerome/Documents/NYU/Capstone/DashOfData/Model/Models"
)
import pandas as pd
from posData_preprocessing import get_posData
from weatherData_preprocessing import get_weatherData
from indicies_preprocessing import get_marketData
#from econData_preprocessing import econData
from sarimax_model import sarimax_model
#from mlp_model import repeat_evaluate, summarize_scores
from holtwinter_model import holtwinter_model
#from get_forecasts import get_forecasts
#import matplotlib.pyplot as plt

# NY
account_id = 1
city_id = 5128581
start_date = '2014-03-01'
end_date = '2018-05-01'

## CT
#account_id = 2
#city_id = 4843564
#start_date = '2018-01-02'
#end_date = '2019-01-30'


posData = get_posData(account_id, start_date, end_date)
weatherData = get_weatherData(city_id, start_date, end_date)
market_data = get_marketData()

# Target variable
target_variable = pd.DataFrame(posData.guests_log_diff)

# External variable - holiday
weatherData['date'] = pd.DatetimeIndex(weatherData.index)
weatherData['holiday'] = 0
import holidays
us_holidays = holidays.US()
for i in weatherData.date:
    if weatherData.date[i] in us_holidays:
            weatherData.holiday[i] = 1

#External variable - weekend diff
weatherData['weekday'] = pd.DatetimeIndex(weatherData.index).dayofweek
weatherData['weekend'] = (weatherData.weekday >3).astype(float)
weatherData["weekend_diff"] = weatherData.weekend - weatherData.weekend.shift(7).fillna(0)


# days to forecast
n_test = 7

# External variables
exog_variables = [
    weatherData.temp_diff,
    weatherData.humidity_diff,
    weatherData.holiday,
#    weatherData.weekend_diff
]

##MLP
## define config
##n_input, n_nodes, n_epochs, n_batch
#config = [7, 500, 100, 100]
#
## grid search
#scores = repeat_evaluate(target_variable, config, n_test)
## summarize scores
#summarize_scores('mlp', scores)

# SARIMAX
sarimax_result = sarimax_model(
    target_variable,
    exog_variables,
    start_date,
    end_date,
    n_test,
    account_id,
    plot=False,
    save=False,
)

# HoltWinter
holtwinter_result = holtwinter_model(
    target_variable, 
    n_test, 
    account_id,
    plot=False, 
    save=False,
    )

# SUMMARY
print("SARIMAX Summary: ", sarimax_result["fit"].summary())
print("Standard Deviation: ", target_variable.std()[0])
print("SARIMAX RMSE_TEST: ", sarimax_result["rmse_test"])
print("HOLTWINTER RMS: ", holtwinter_result["rms"])


## Plot Forecasts vs Actual Demand
#
#
## Query transformed forecasts
#model = 'sarimax'
#target_variable = 'guests_log_diff_val'
#td = get_forecasts(account_id, target_variable, model)
#td = pd.DataFrame(
#        td,
#        columns=[
#            "date",
#            "guests",
#        ],
#        dtype=int,
#    )
#
#
## Set Index
#td["date"] = pd.to_datetime(td["date"])
#td.index = td["date"]
##td.drop("datetime", axis=1, inplace=True)
#td = td.rename(columns={'guests' : 'forecast'})
#posData = get_posData(account_id, start_date, end_date)
#actuals = pd.DataFrame(posData.guests)
#actuals['date'] = actuals.index
#td_ma = td.merge(actuals, left_index=True, right_index = True)
#td_ma = td_ma.groupby('date_x').mean()
#
## Plot
#x = td_ma.guests 
#y = td_ma.forecast
#plt.figure(figsize=(16, 8))
#plt.plot(x.iloc[-7:], label="Actual")
#plt.plot(y.iloc[-7:], label="Forecast - SARIMA")
#
