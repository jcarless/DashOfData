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

account_id = 1

#Target variable
target_variable = pd.DataFrame(posData.guests_diff)

# data split
n_test = 7

#External variables
exog_variables = [
          posData.severity_diff,
          posData.humidity_diff,
          ind.FXG.FXG_close_diff_lag7
        ]

#SARIMAX
sarimax_result = sarimax_model(target_variable, 
                               exog_variables,  
                               start_date, 
                               end_date, 
                               n_test, 
                               False,
                               False,
                               account_id
                               )

#HoltWinter
#holtwinter_result = holtwinter_model(target_variable, n_test, False)

#SUMMARY
print("SARIMAX Summary: ", sarimax_result["fit"].summary())
print("Standard Deviation: ", target_variable.std()[0])
print("SARIMAX RMSE_TEST: ", sarimax_result["rmse_test"])
#print("HOLTWINTER RMS: ", holtwinter_result["rms"])

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