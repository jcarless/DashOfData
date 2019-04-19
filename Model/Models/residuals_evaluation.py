import os
import sys
sys.path.append("Model/PreProcessing")
sys.path.append("Model/Models")
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
from posData_preprocessing import get_posData
from weatherData_preprocessing import get_weatherData
from indicies_preprocessing import get_marketData
from econData_preprocessing import econData
from sarimax_model import sarimax_model
#from mlp_model import series_to_supervised, repeat_evaluate, summarize_scores
from holtwinter_model import holtwinter_model
#from dod_model import sarimax_result, holtwinter_result
from datetime import timedelta, date, datetime
from itertools import chain
from random import randrange
from matplotlib import pyplot
import holidays
from get_forecasts import get_forecasts
import matplotlib.pyplot as plt
import seaborn as sns

# Select location

## NY
#account_id = 1
#city_id = 5128581
#start_date = '2014-03-01'
#end_date = '2018-05-01'
#later_d = '2014-09-02' # - NY


# CT
account_id = 2
city_id = 4843564
start_date = '2018-01-02'
end_date = '2019-01-30'
later_d = '2018-07-02' # - CT




# Walk forward validation


# Create range of dates
dates = []
start_dt = datetime.strptime(later_d, '%Y-%m-%d').date()
end_dt = datetime.strptime(end_date, '%Y-%m-%d').date()

#Number of dates
def random_date(start, end, n_d):
    for n in range(1,n_d):
        delta = end - start
        int_delta = delta.days
        random_d = randrange(int_delta)
        dates.append((start + timedelta(days=random_d)).strftime('%Y-%m-%d'))
    return 


#Number of evaluations
n_d = 7

random_date(start_dt, end_dt, n_d)

sarimax_d = {}

# days to forecast
n_test = 7

#sarimax_e = {
#        "rmse_test": "",
#        "rmse_train": "",
#        "fit": "",
#        "actual": "",
#        "prediction": "",
#        }
sarimax_r = []

us_holidays = holidays.US()
    
h_calendar = get_weatherData(city_id, start_date, end_date)
#h_calendar = pd.DataFrame(index = pd.date_range(start_date, end_date, freq = 'D'))
h_calendar['date'] = h_calendar.index
h_calendar['holiday'] = 0
for i in h_calendar.date:
    if h_calendar.date[i] in us_holidays:
        h_calendar.holiday[i] = 1
        

for i in range(len(dates)):
    posData = get_posData(account_id, start_date, dates[i])
    weatherData = get_weatherData(city_id, start_date, dates[i])
    holiday = h_calendar.loc[start_date:dates[i]]
    weatherData['weekday'] = pd.DatetimeIndex(weatherData.index).dayofweek
    weatherData['weekend'] = (weatherData.weekday >3).astype(float)
    weatherData["weekend_diff"] = weatherData.weekend - weatherData.weekend.shift(7).fillna(0)
    exog_variables = [weatherData.temp_diff,
                      weatherData.humidity_diff,
#                      weatherData.weekend_diff,
                      holiday.holiday
                      ]
    target_variable = pd.DataFrame(posData.guests_log_diff)
    target_variable = target_variable.rename(columns={'guests_log_diff' : 'guests_log_diff_val'})
    sarimax_d = sarimax_model(target_variable,
                                   exog_variables,
                                   start_date,
                                   dates[i],
                                   n_test,
                                   account_id,
                                   plot=False,
                                   save=True)
#    sarimax_r.append(sarimax_d)
    



## Analyses of Residuals

pr = []
ac = []
a = []
for i in range(len(sarimax_r)):
    pr.append(sarimax_r[i]['prediction'])
    ac.append(sarimax_r[i]['actual'])

prediction = pr[1]
actual = ac[1]
for i in range(len(sarimax_r)):
    prediction = prediction.append(pr[i])
    actual = actual.append(ac[i])
    
#prediction = sarimax_r['prediction']
#actual = target_variable.tail(n_test)
#actual = sarimax_r['actual']

#comparison = actual.merge(prediction.to_frame(), left_index=True, right_index=True)
comparison = pd.concat([actual, prediction], axis = 1)

#residuals = [actual['guests_log_diff'][i]-prediction['SARIMA'][i] for i in range(len(actual))]
residuals = [comparison['guests_log_diff_val'][i]-comparison['SARIMA'][i] for i in range(len(comparison))]
residuals = pd.DataFrame(residuals)

residuals.plot()
pyplot.show()

# Residual plot does not show a trend, seasonal or cyclic structure, which means our model 
#is not missing any further time series analysis


## Residual summary statistics

res_summary = residuals.describe()

# Residual histogram and density plots
residuals.hist()
pyplot.show()

residuals.plot(kind='kde')
pyplot.show()


# Autocorrelation plot
from pandas.tools.plotting import autocorrelation_plot
autocorrelation_plot(residuals)
pyplot.show()




# Evaluation of Transformed Forecasts vs Actuals

# Query transformed forecasts
model = 'sarimax'
target_variable = 'guests_log_diff_val'
td = get_forecasts(account_id, target_variable, model)
td = pd.DataFrame(
        td,
        columns=[
            "date",
            "guests",
        ],
        dtype=int,
    )

# Set Index
td["date"] = pd.to_datetime(td["date"])
td.index = td["date"]
td = td.rename(columns={'guests' : 'forecast'})
posData = get_posData(account_id, start_date, end_date)
actuals = pd.DataFrame(posData.guests)
actuals['date'] = actuals.index
td_ma = td.merge(actuals, left_index=True, right_index = True)
td_ma['weekday'] = pd.DatetimeIndex(td_ma.index).day_name()
td_ma['wd'] = pd.DatetimeIndex(td_ma.index).dayofweek

# Delta (Actual - Forecast)
td_ma['delta'] = td_ma.guests - td_ma.forecast
td_avg = td_ma.groupby(td_ma.index).mean()
td_avg['weekday'] = pd.DatetimeIndex(td_avg.index).day_name()
td_avg_w = td_avg.groupby('weekday').mean()

#
###Scatter
#plt.figure(figsize=(16, 8))
#x = td_ma.guests 
#y = td_ma.forecast
#plt.scatter(x, y, c=td_ma.wd, cmap = plt.cm.autumn)
#plt.colorbar()
##z = np.polyfit(x, y, 1)
##p = np.poly1d(z)
##plt.plot(x,p(x),"r--")
#plt.show()


# Boxplot
plt.figure(figsize=(16, 8))
sns.set(style="whitegrid")
ax = sns.boxplot(x='weekday', y='delta', data=td_ma, order = [
        'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])