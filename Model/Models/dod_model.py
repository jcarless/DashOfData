import os
import sys

sys.path.append(
    "/Users/jerome/Documents/NYU/Capstone/DashOfData/Model/PreProcessing"
)
sys.path.append("Model/Models")
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
from posData_preprocessing import get_posData
from weatherData_preprocessing import get_weatherData
import indicies_preprocessing as ind
from econData_preprocessing import econData
from sarimax_model import sarimax_model

# from mlp_model import series_to_supervised, repeat_evaluate, summarize_scores
from holtwinter_model import holtwinter_model

start_date = '2018-02-01'
end_date = '2018-05-01'

# NY
account_id = 1
city_id = 5128581

## CT
#account_id = 2
#city_id = 4843564

posData = get_posData(account_id, start_date, end_date)
weatherData = get_weatherData(city_id, start_date, end_date)

# Target variable
target_variable = pd.DataFrame(posData.guests_diff)

# days to forecast
n_test = 7

# External variables
exog_variables = [
    weatherData.severity_diff,
    weatherData.humidity_diff,
    ind.FXG.FXG_close_diff_lag7,
]

# SARIMAX
sarimax_result = sarimax_model(
    target_variable,
    exog_variables,
    start_date,
    end_date,
    n_test,
    account_id,
    plot=True,
    save=False,
)

# HoltWinter
holtwinter_result = holtwinter_model(target_variable, n_test, False)

# SUMMARY
print("SARIMAX Summary: ", sarimax_result["fit"].summary())
print("Standard Deviation: ", target_variable.std()[0])
print("SARIMAX RMSE_TEST: ", sarimax_result["rmse_test"])
# print("HOLTWINTER RMS: ", holtwinter_result["rms"])

##MLP
## define config
##n_input, n_nodes, n_epochs, n_batch
# config = [7, 500, 100, 100]
#
### grid search
##scores = repeat_evaluate(target_variable, config, n_test)
##
### summarize scores
##summarize_scores('persistence', scores)
#
## grid search
# scores = repeat_evaluate(target_variable, config, n_test)
## summarize scores
# summarize_scores('mlp', scores)

