#import os, sys
#sys.path.append("Model/PreProcessing")
#sys.path.append(
#    "/Users/jerome/Documents/NYU/Capstone/DashOfData/Model/PreProcessing"
#)
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from posData_preprocessing import get_posData
from weatherData_preprocessing import get_weatherData
from indicies_preprocessing import get_marketData
from econData_preprocessing import econData
import pandas as pd
from lags import lags
from kpss_test import kpss_test
from adf_test import adf_test
import numpy as np
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
marketData = get_marketData()

print("KPSS TEST: ", kpss_test(posData["guests"], plot = False))
print("ADF TEST: ", adf_test(posData["guests"]))

df = pd.DataFrame()
df["guests"] = posData['guests']
#df["guests_log"] = posData['guests_log']
df["guests_log_diff"] = posData['guests_log_diff']
#df["guests_log"] = posData['guests_log']
#df["temp"] = weatherData["temp"]
df["temp_diff"] = weatherData["temp_diff"]
#df["severity"] = weatherData["severity"]
#df["severity_diff"] = weatherData["severity_diff"]
#df["GDP"] = econData["gdp"]
#df["total_sales"] = posData['total_sales']
df["humidity_diff"] = weatherData['humidity_diff']
#df["guests_diff"] = posData['guests_diff']
#df["temp_diff"] = weatherData['temp_diff']
#df["guests_diff_percent"] = posData['guests_diff_percent']
#df["temp_diff_percent"] = weatherData['temp_diff_percent']

#for fund in marketData:
#    df = lags(fund, fund["symbol"][0]).join(df, on=None, how="right")

correlation_matrix = df.corr(method = "pearson")




## 30 day average
#df_r30 = df.rolling(window=30).mean()
#
#r30 = df.merge(df_r30, left_index = True, right_index = True)
#
#r30 = r30.drop(r30.index[:30])
#
#corr_matrix_r30 = r30.corr(method = "pearson")



# Indexes

## 30 day average indexes
#r30_i = pd.DataFrame()
##r30_i['guests'] = r30['guests_x']
#r30_i['temp'] = r30['temp_x']
#r30_i['GDP'] = r30['GDP_x']
#r30_i['severity'] = r30['severity_x']
#r30_i['humidity'] = r30['humidity_x']
#r30_i['total_sales'] = r30['total_sales_x']
#r30_i['guests_log_diff'] = r30['guests_log_diff_x']
#r30_i['temp_diff'] = r30['temp_diff_x']
#r30_i['severity_diff'] = r30['severity_diff_x']
#r30_i['humidity_dff'] = r30['humidity_diff_x']
##r30_i['ind_guests'] = r30.guests_x / r30.guests_y *100
#r30_i['ind_temp'] = r30.temp_x / r30.temp_y *100
#r30_i['ind_GDP'] = r30.GDP_x / r30.GDP_y *100
#r30_i['ind_severity'] = r30.severity_x / r30.severity_y *100
#r30_i['ind_humidity'] = r30.humidity_x / r30.humidity_y *100
#r30_i['ind_total_sales'] = r30.total_sales_x / r30.total_sales_y *100
#r30_i['ind_guests_log_diff'] = r30.guests_log_diff_x / r30.guests_log_diff_y *100
#r30_i['ind_temp_diff'] = r30.temp_diff_x / r30.temp_diff_y *100
#r30_i['ind_severity_diff'] = r30.severity_diff_x / r30.severity_diff_y *100
#r30_i['ind_humidity_diff'] = r30.humidity_diff_x / r30.humidity_diff_y *100
#
#corr_matrix_r30_i = r30_i.corr(method = "pearson")


# Monthly average (calendar month)
df_ma = df
df_ma['year'] = pd.DatetimeIndex(df_ma.index).year
df_ma['month'] = pd.DatetimeIndex(df_ma.index).month
df_ma['day'] = pd.DatetimeIndex(df_ma.index).day
df_ma['weekday'] = pd.DatetimeIndex(df_ma.index).dayofweek
df_ma['yearmonth'] = pd.to_datetime(df_ma[['year', 'month']].assign(Day=1))
df_ma['date'] = pd.DatetimeIndex(df_ma.index)
df_ma['holiday'] = 0
import holidays
us_holidays = holidays.US()
for i in df_ma.date:
    if df_ma.date[i] in us_holidays:
            df_ma.holiday[i] = 1



df_ma['pre_holiday'] = df_ma.holiday.shift(-1)
df_ma['post_holiday'] = df_ma.holiday.shift(1)
df_ma['near_holiday'] = df_ma.pre_holiday + df_ma.post_holiday
df_ma = df_ma.drop(['pre_holiday', 'post_holiday', 'date'], axis=1)
df_ma['ext_holiday'] = df_ma.holiday + df_ma.near_holiday

df_ma['monday'] = df_ma.weekday == 0
df_ma['tuesday'] = df_ma.weekday == 1
df_ma['wednesday'] = df_ma.weekday == 2
df_ma['thursday'] = df_ma.weekday == 3
df_ma['friday'] = df_ma.weekday == 4
df_ma['saturday'] = df_ma.weekday == 5
df_ma['sunday'] = df_ma.weekday == 6

df_ma['weekend'] = (df_ma.weekday >3).astype(float)
df_ma["weekend_log"] = np.log(df_ma.weekend).fillna(0)
df_ma["weekend_diff"] = df_ma.weekend - df_ma.weekend.shift(7).fillna(0)
    

def to_integer(dt_time):
    return 10000*pd.DatetimeIndex(dt_time).year + 100*pd.DatetimeIndex(dt_time).month

df_ma.yearmonth = to_integer(df_ma.yearmonth)

mon_avg = df_ma.groupby('yearmonth').mean()
mon_avg = mon_avg.drop(['year', 'month', 'day', 'weekday'], axis=1)

df_ma = df_ma.merge(mon_avg, on='yearmonth', how='right')

corr_matrix_ma = df_ma.corr(method = "pearson")

df_ma_i = df_ma
df_ma_i['ind_severity'] = df_ma.severity_x / df_ma.severity_y *100
df_ma_i['ind_humidity'] = df_ma.humidity_x / df_ma.humidity_y *100
df_ma_i['ind_total_sales'] = df_ma.total_sales_x / df_ma.total_sales_y *100
df_ma_i['ind_guests_log_diff'] = df_ma.guests_log_diff_x / df_ma.guests_log_diff_y *100
df_ma_i['ind_temp_diff'] = df_ma.temp_diff_x / df_ma.temp_diff_y *100
df_ma_i['ind_severity_diff'] = df_ma.severity_diff_x / df_ma.severity_diff_y *100
df_ma_i['ind_humidity_diff'] = df_ma.humidity_diff_x / df_ma.humidity_diff_y *100

df_ma_i = df_ma_i.drop(['year', 'month','day', 'weekday', 'yearmonth','temp_y', 
                        'severity_y', 'humidity_y',
                        'GDP_y', 'total_sales_y', 'guests_log_diff_y', 'humidity_diff_y',
                        'temp_diff_y', 'severity_diff_y'], axis=1)
corr_matrix_ma_i = df_ma_i.corr(method = "pearson")