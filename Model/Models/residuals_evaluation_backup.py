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

## NY
#account_id = 1
#city_id = 5128581
#start_date = '2014-03-01'
#end_date = '2018-05-01'

# CT
account_id = 2
city_id = 4843564
start_date = '2018-01-02'
end_date = '2019-01-30'

#posData = get_posData(account_id, start_date, end_date)
#weatherData = get_weatherData(city_id, start_date, end_date)
#market_data = get_marketData()
#
## Target variable
#target_variable = pd.DataFrame(posData.guests_log_diff)
#
## days to forecast
#n_test = 7
#
##ex = market_data[6]["FXG_close_diff_lag7"].tail(90).astype("float")
#
## External variables
#exog_variables = [
#    weatherData.temp_diff,
#    weatherData.humidity_diff,
##    econData.gdp.tail(90).astype("float"),
#]
#




# Walk forward validation


# Create range of dates
dates = []
later_d = '2018-07-02' # - CT
#later_d = '2014-09-02' # - NY

start_dt = datetime.strptime(later_d, '%Y-%m-%d').date()
end_dt = datetime.strptime(end_date, '%Y-%m-%d').date()

# Original
#def random_date(start, end):
#    """
#    This function will return a random datetime between two datetime 
#    objects.
#    """
#    delta = end - start
#    int_delta = delta.days
#    random_d = randrange(int_delta)
#    return start + timedelta(days=random_d)

##Appended
#def random_date(start, end):
#    """
#    This function will return a random datetime between two datetime 
#    objects.
#    """
#    delta = end - start
#    int_delta = delta.days
#    random_d = randrange(int_delta)
#    dates.append(start + timedelta(days=random_d))
#    return 

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


#for i in range(len(dates)):
#    sarimax_d = sarimax_model(target_variable,
#                                   exog_variables,
#                                   start_date,
#                                   dates[i],
#                                   n_test,
#                                   account_id,
#                                   plot=False,
#                                   save=False)
#    sarimax_result.append(sarimax_d)

sarimax_d = {}
# days to forecast
n_test = 7

sarimax_e = {
        "rmse_test": "",
        "rmse_train": "",
        "fit": "",
        "actual": "",
        "prediction": "",
        }
sarimax_r = []

us_holidays = holidays.US()
#h_calendar = pd.DataFrame()
h_calendar['date'] = pd.date_range(start_date, end_date, freq = 'D')
h_calendar = pd.DataFrame(index = pd.date_range(start_date, end_date, freq = 'D'))
h_calendar['date'] = h_calendar.index
h_calendar['holiday'] = 0



h_calendar['date'] = pd.date_range(start_date, end_date, freq = 'D')
h_calendar["date"] = pd.to_datetime(h_calendar["date"])
h_calendar['holiday'] = 0
h_calendar.index = h_calendar.date
for i in h_calendar.date:
        if h_calendar.date[i] in us_holidays:
            h_calendar.holiday[i] = 1
    
def holiday_check(start_date, end_date):
    h_calendar = pd.DataFrame(index = pd.date_range(start_date, end_date, freq = 'D'))
    h_calendar['date'] = h_calendar.index
    h_calendar['holiday'] = 0
    for i in h_calendar.date:
        if h_calendar.date[i] in us_holidays:
            h_calendar.holiday[i] = 1
    
holiday_check(start_date, end_date)
test = h_calendar.loc[start_date:dates[1]]

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
    sarimax_d = sarimax_model(target_variable,
                                   exog_variables,
                                   start_date,
                                   dates[i],
                                   n_test,
                                   account_id,
                                   plot=False,
                                   save=False)
    sarimax_r.append(sarimax_d)
    

#
#for i in range(len(dates)):
#    posData = get_posData(account_id, start_date, dates[i])
#    weatherData = get_weatherData(city_id, start_date, dates[i])
#    exog_variables = [weatherData.temp_diff,
#                      weatherData.humidity_diff,
#                      ]
#    target_variable = pd.DataFrame(posData.guests_log_diff)
#    sarimax_d = sarimax_model(target_variable,
#                                   exog_variables,
#                                   start_date,
#                                   dates[i],
#                                   n_test,
#                                   account_id,
#                                   plot=False,
#                                   save=False)
#    sarimax_r.append(sarimax_d)
#    

## Residual line plot

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
    
#    prediction = pr[i]['prediction'] + prediction
#    actual = ac[i]['actual'] + actual
#a = pr[1].append(pr[2])
#a = a.append(pr[3])

 
#prediction = sarimax_r['prediction']
#actual = target_variable.tail(n_test)
#actual = sarimax_r['actual']

#comparison = actual.merge(prediction.to_frame(), left_index=True, right_index=True)
comparison = pd.concat([actual, prediction], axis = 1)

#residuals = [actual['guests_log_diff'][i]-prediction['SARIMA'][i] for i in range(len(actual))]
residuals = [comparison['guests_log_diff'][i]-comparison['SARIMA'][i] for i in range(len(comparison))]
residuals = pd.DataFrame(residuals)

residuals.plot()
pyplot.show()

# Residual plot does not show a trend, seasonal or cyclic structure, which means our model 
#is not missing any further time series analysis


## Residual summary statistics

print(residuals.describe())

# Residual histogram and density plots
residuals.hist()
pyplot.show()

residuals.plot(kind='kde')
pyplot.show()

## Q-Q plot
#from statsmodels.graphics.gofplots import qqplot
#import numpy
#residuals2 = numpy.array(residuals)
#qqplot(residuals2)
#pyplot.show()

# Autocorrelation plot
from pandas.tools.plotting import autocorrelation_plot
autocorrelation_plot(residuals)
pyplot.show()
