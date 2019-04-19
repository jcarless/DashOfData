import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append("Model/Models")
sys.path.append("Model/PreProcessing")
import statsmodels.api as sm
import numpy as np
import pandas as pd
from posData_preprocessing import get_posData
from weatherData_preprocessing import get_weatherData
from indicies_preprocessing import get_marketData
import psycopg2
from psycopg2.extensions import AsIs
import datetime
from db_functions import db_connection, db_close
import indicies_preprocessing as ind
from itertools import product
from tqdm import tqdm_notebook

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


def train_test_split(data, n_test):
	return data[:-n_test], data[-n_test:]

exog_variables = np.column_stack((
          weatherData['temp_diff'].values,
          weatherData['humidity_diff'].values,
#          ind.FXG['FXG_close_diff'].values
        ))

#### setting initial values and some bounds for them
ps = range(3, 5) # last significant lag on Partial Autocorrelation plot
    #p is equal to the first lag where the PACF value is above the significance level.

d=1 # number of differences used 
    #d=0 if the series has no visible trend or ACF at all lags is low.
    #d≥1 if the series has visible trend or positive ACF values out to a high number of lags.
qs = range(1, 3) # set range between number of steps in sequence on the Autocorrelation plot
    # q is equal to the first lag where the ACF value is above the significance level.
Ps = range(0, 2) # number of significant lags on the Partial Autocorrelation plot
    # P≥1 if the ACF is positive at lag S, else P=0.
D=1  # 1 as we performed seasonal differentiation
    # D=1 if the series has a stable seasonal pattern over time.
    # D=0 if the series has an unstable seasonal pattern over time.
Qs = range(0, 2) # set range between values that exceed the plot (except for x=0)
    # Q≥1 if the ACF is negative at lag S, else Q=0
s = 7 # season length is 7
    # S is equal to the ACF lag with the highest value (typically at a high lag)

# creating list with all the possible combinations of parameters
parameters = product(ps, qs, Ps, Qs)
parameters_list = list(parameters)
len(parameters_list)

def optimizeSARIMA(parameters_list, d, D, s):
    """
        Return dataframe with parameters and corresponding AIC
        
        parameters_list - list with (p, q, P, Q) tuples
        d - integration order in ARIMA model
        D - seasonal integration order 
        s - length of season
    """
    
    results = []
    best_aic = float("inf")

    for param in tqdm_notebook(parameters_list):
        # we need try-except because on some combinations model fails to converge
        try:
            model = sm.tsa.SARIMAX(posData["guests_log_diff"], exog= exog_variables, enforce_invertibility=False, order=(param[0], d, param[1]), 
                                            seasonal_order=(param[2], D, param[3], s)).fit(disp=1)
            aic = model.aic
            print("AIC: ", aic)
            # saving best model, AIC and parameters
            if aic < best_aic:
                best_aic = aic
                results.append([param, model.aic])
        except Exception:
            continue

    result_table = pd.DataFrame(results)
    result_table.columns = ['parameters', 'aic']
    # sorting in ascending order, the lower AIC is - the better
    result_table = result_table.sort_values(by='aic', ascending=True).reset_index(drop=True)
    
    return result_table
         
conn, cur = db_connection()
    
try:
    # Run function to determine best paremeters
    result_table = optimizeSARIMA(parameters_list, d, D, s)
    
    result_table.head()
    
    
    p, q, P, Q = result_table.parameters[0]
    
    ### List of parameters to export 
    order_parameters = [p, d, q]
    seasonal_order = [P, D, Q, s]
    
except Exception as error:
    raise error
    
try:
    sql = f"""INSERT INTO %s(model_category,date,p_,d_,q_,P,D,Q,s,account_id)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    
    cur.execute(sql, 
    (AsIs('model_parameters'), 
    "sarimax",
    datetime.datetime.now(),
    p,d,q,P,D,Q,s,
    account_id))


    # close communication with the PostgreSQL database server
    cur.close()

    # commit the changes
    conn.commit()

except (Exception, psycopg2.DatabaseError) as error:
    raise error
    
#End the session
db_close(conn)

