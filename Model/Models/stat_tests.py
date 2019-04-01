import os, sys
sys.path.append("Model/PreProcessing")
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from posData_preprocessing import get_posData
from weatherData_preprocessing import get_weatherData
import indicies_preprocessing as ind
from econData_preprocessing import econData
import pandas as pd
from lags import lags
from kpss_test import kpss_test
from adf_test import adf_test

start_date = '2018-02-01'
end_date = '2018-05-01'

# NY
account_id = 1
city_id = 5128581

## CT
# account_id = 2
# city_id = 4843564

posData = get_posData(account_id, start_date, end_date)
weatherData = get_weatherData(city_id, start_date, end_date)

print("KPSS TEST: ", kpss_test(posData["guests_diff"], plot = False))
print("ADF TEST: ", adf_test(posData["guests_diff"]))

#ind.IYK["GDP"] = econData["gdp"]
df = pd.DataFrame()
df["guests_log_diff"] = posData['guests_log_diff']
df["guests_log"] = posData['guests_log']
df["temp"] = weatherData["temp"]
df["severity"] = weatherData["severity"]
df["GDP"] = econData["gdp"]
df["total_sales"] = posData['total_sales']
df["humidity"] = weatherData['humidity']
df["guests_diff"] = posData['guests_diff']
df["temp_diff"] = weatherData['temp_diff']
df["guests_diff_percent"] = posData['guests_diff_percent']
df["temp_diff_percent"] = weatherData['temp_diff_percent']

QQQ_lag = lags(ind.QQQ, "QQQ")
IYK_lag = lags(ind.IYK, "IYK")
XLY_lag = lags(ind.XLY, "XLY")
PBJ_lag = lags(ind.PBJ, "PBJ")
FSTA_lag = lags(ind.FSTA, "FSTA")
FXG_lag = lags(ind.FXG, "FXG")

df = QQQ_lag.join(df, on=None, how="left")
df = IYK_lag.join(df, on=None, how="left")
df = XLY_lag.join(df, on=None, how="left")
df = PBJ_lag.join(df, on=None, how="left")
df = FSTA_lag.join(df, on=None, how="left")
df = FXG_lag.join(df, on=None, how="left")

test = pd.DataFrame()
test["guests_diff"] = df["guests_diff"]
test["humidity"] = df["humidity"]
test["severity"] = df["severity"]
test["humidity"] = df["humidity"]
test["FXG_close_diff"] = df["FXG_close_diff"]

correlation_matrix = test.corr(method = "pearson")