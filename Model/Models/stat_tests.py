import os, sys
sys.path.append("Model/PreProcessing")
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from posData_preprocessing import posData
import indicies_preprocessing as ind
from econData_preprocessing import econData
import pandas as pd
from lags import lags
from kpss_test import kpss_test
from adf_test import adf_test

print("KPSS TEST: ", kpss_test(posData["guests_diff"]))
print("ADF TEST: ", adf_test(posData["guests_diff"]))

#ind.IYK["GDP"] = econData["gdp"]
df = pd.DataFrame()
df["guests_log_diff"] = posData['guests_log_diff']
df["guests_log"] = posData['guests_log']

QQQ_lag = lags(ind.QQQ, "QQQ")
IYK_lag = lags(ind.IYK, "IYK")
XLY_lag = lags(ind.XLY, "XLY")
PBJ_lag = lags(ind.PBJ, "PBJ")
FSTA_lag = lags(ind.FSTA, "FSTA")
FXG_lag = lags(ind.FXG, "FXG")

df["temp"] = posData["temp"]
df["severity"] = posData["severity"]
df["GDP"] = econData["gdp"]
df["total_sales"] = posData['total_sales']
df["humidity"] = posData['humidity']

df["guests_diff"] = posData['guests_diff']
df["temp_diff"] = posData['temp_diff']
df["guests_diff_percent"] = posData['guests_diff_percent']
df["temp_diff_percent"] = posData['temp_diff_percent']

df = QQQ_lag.join(df, on=None, how="left")
df = IYK_lag.join(df, on=None, how="left")
df = XLY_lag.join(df, on=None, how="left")
df = PBJ_lag.join(df, on=None, how="left")
df = FSTA_lag.join(df, on=None, how="left")
df = FXG_lag.join(df, on=None, how="left")


correlation_matrix = df.corr(method = "pearson")