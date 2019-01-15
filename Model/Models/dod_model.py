import os, sys
sys.path.append("Model/PreProcessing")
sys.path.append("Model/Models")
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config_model import start_date, end_date
from posData_preprocessing import posData
import indicies_preprocessing as ind
from econData_preprocessing import econData
from sarimax_model import sarimax_model
from mlp_model import series_to_supervised, repeat_evaluate, summarize_scores
from holtwinter_model import holtwinter_model
import pandas as pd
import numpy as np


#DF Column names
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

# data split
n_test = 7

#Target variable series we are trying to predict
target_variable = pd.DataFrame(posData["guests_log_diff"])
print("target_variable Standard Deviation: ", np.std(target_variable))

#External variables used in predictions
exog_variables = [
#          posData['temp_log_diff'],
          posData['severity'],
#          posData['humidity'],
##          ind.IYK['close'],
##          ind.RHS['close'],
##          ind.FSTA['close'],
##          ind.VDC['close'],
##          ind.PBJ['close'],
##          ind.XLY['close'],
##          ind.FXG['close'],
##          ind.QQQ['close'],
##          econData['gdp']
        ]

#SARIMAX
sarimax_result = sarimax_model(target_variable, 
                               exog_variables,  
                               start_date, 
                               end_date, 
                               n_test, 
                               True
                               )

#print("SARIMAX RMSE_TRAIN: ", sarimax_result["rmse_train"])
#print("SARIMAX RMSE_TEST: ", sarimax_result["rms"])




#HoltWinter
holtwinter_result = holtwinter_model(target_variable, n_test, True)


#SUMMARY
print("SARIMAX Summary: ", sarimax_result["fit"].summary())
print("SARIMAX RMSE_TEST: ", sarimax_result["rmse_test"])
print("HOLTWINTER RMS: ", holtwinter_result["rms"])


##MLP
## define config
##n_input, n_nodes, n_epochs, n_batch
#config = [7, 500, 100, 100]
#
### grid search
##scores = repeat_evaluate(target_variable, config, n_test)
##
### summarize scores
##summarize_scores('persistence', scores)
#
## grid search
#scores = repeat_evaluate(target_variable, config, n_test)
## summarize scores
#summarize_scores('mlp', scores)


