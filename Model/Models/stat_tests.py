import os, sys
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
marketData = get_marketData()

print("KPSS TEST: ", kpss_test(posData["guests_diff"], plot = False))
print("ADF TEST: ", adf_test(posData["guests_diff"]))

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

for fund in marketData:
    df = lags(fund, fund["symbol"][0]).join(df, on=None, how="right")

#test = pd.DataFrame()
#test["guests_diff"] = df["guests_diff"]
#test["humidity"] = df["humidity"]
#test["severity"] = df["severity"]
#test["humidity"] = df["humidity"]
#test["FXG_close_diff"] = df["FXG_close_diff"]

correlation_matrix = df.corr(method = "pearson")