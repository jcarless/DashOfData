import os, sys
sys.path.append("Model/Models")
sys.path.append("Model/PreProcessing")
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#import dod_model as m
#from config_model import start_date, end_date
#from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import statsmodels.api as sm
#from math import sqrt
import numpy as np
import pandas as pd
from posData_preprocessing import get_posData
from weatherData_preprocessing import get_weatherData
from indicies_preprocessing import get_marketData
from econData_preprocessing import econData
import psycopg2
from psycopg2.extensions import AsIs
import datetime

# config
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0
    
import os

def config(filename='Model/database.ini', section='postgresql'):
    if os.path.isfile(filename):
        # create a parser
        parser = ConfigParser()
        # read config file
        parser.read(filename)
        
        # get section, default to postgresql
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    else:
        raise Exception(f"Config file {filename} not found")
 
    return db

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

exog_train=[]


import indicies_preprocessing as ind


def train_test_split(data, n_test):
	return data[:-n_test], data[-n_test:]

weatherData = get_weatherData(city_id, start_date, end_date)

exog_variables = np.column_stack((
          weatherData.temp_diff,
          weatherData.humidity_diff,
        ))

target_variable = pd.DataFrame(posData.guests_log_diff)

model_train_ts = target_variable
#
#exog_train = np.column_stack((
#                              m.train['temp_diff'].values,
#                              m.train['severity'].values,
#                              m.train['humidity'].values,
#                              m.train['high_temp'].values,
#                              m.IYK_train['close'].values,
#                              m.RHS_train['close'].values,
#                              m.FSTA_train['close'].values,
#                              m.VDC_train['close'].values,
#                              m.PBJ_train['close'].values,
#                              m.XLY_train['close'].values,
#                              m.FXG_train['close'].values,
#                              m.econ_train['gdp'].values
#                              ))
#
#exog_test = np.column_stack((
#                             m.test['temp'].values,
#                             m.test['severity'].values,
#                             m.test['humidity'].values,
#                             m.test['high_temp'].values,
#                             m.IYK_test['close'].values,
#                             m.RHS_test['close'].values,
#                             m.FSTA_test['close'].values,
#                             m.VDC_test['close'].values,
#                             m.PBJ_test['close'].values,
#                             m.XLY_test['close'].values,
#                             m.FXG_test['close'].values,
#                             m.econ_test['gdp'].values
#                             ))

#y_hat_avg = m.test.copy()
#fit1 = sm.tsa.SARIMAX(model_train_ts, exog=exog_train, order=(2,0,0), seasonal_order=(1, 1, 1, 12)).fit()
#print("SARIMAX SUMMARY: ",fit1.summary())
#y_hat_avg['SARIMA'] = fit1.predict(exog=exog_test, start = start_date, end = end_date, dynamic=True)
#plt.figure(figsize=(16,8))
#plt.plot(m.train['guests'], label='dod_model.Train')
#plt.plot(m.test['guests'], label='Test')
#plt.plot(y_hat_avg['SARIMA'], label='SARIMA')
#plt.legend(loc='best')
#plt.show()
#
#fit1.plot_diagnostics(figsize=(15, 12))
#plt.show()

import statsmodels.formula.api as smf            # statistics and econometrics
import statsmodels.tsa.api as smt
import statsmodels.api as sm
import scipy.stats as scs

from itertools import product                    # some useful functions
from tqdm import tqdm_notebook
#
%matplotlib inline

# Dickey-Fuller test plot function
def tsplot(y, lags=None, figsize=(12, 7), style='bmh'):
    """
        Plot time series, its ACF and PACF, calculate Dickey–Fuller test
        
        y - timeseries
        lags - how many lags to include in ACF, PACF calculation
    """
    if not isinstance(y, pd.Series):
        y = pd.Series(y)
        
    with plt.style.context(style):    
        fig = plt.figure(figsize=figsize)
        layout = (2, 2)
        ts_ax = plt.subplot2grid(layout, (0, 0), colspan=2)
        acf_ax = plt.subplot2grid(layout, (1, 0))
        pacf_ax = plt.subplot2grid(layout, (1, 1))
        
        y.plot(ax=ts_ax)
        p_value = sm.tsa.stattools.adfuller(y)[1]
        ts_ax.set_title('Time Series Analysis Plots\n Dickey-Fuller: p={0:.5f}'.format(p_value))
        smt.graphics.plot_acf(y, lags=lags, ax=acf_ax)
        smt.graphics.plot_pacf(y, lags=lags, ax=pacf_ax)
        plt.tight_layout()
        
        
## Test whether data is stationary or not (p value lower than 0.05 means it is stationary)
tsplot(posData["guests"], lags = 60)
tsplot(posData["guests_diff"], lags = 60)
tsplot(posData["guests_log"], lags = 60)
tsplot(posData["guests_log_diff"], lags = 60)


## First differences
#guests_diff = guests_diff - guests_diff.shift(1)
##tsplot(guests_diff[52+1:], lags=60)
#
## Second differences
#guests_diff = guests_diff - guests_diff.shift(1)
##tsplot(guests_diff[52+2:], lags=60)


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
D=0  # 1 as we performed seasonal differentiation
    # D=1 if the series has a stable seasonal pattern over time.
    # D=0 if the series has an unstable seasonal pattern over time.
Qs = range(0, 2) # set range between values that exceed the plot (except for x=0)
    # Q≥1 if the ACF is negative at lag S, else Q=0
s = 52 # season length is 24
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
            model = sm.tsa.SARIMAX(target_variable, exog= exog_variables, enforce_invertibility=False, order=(param[0], d, param[1]), 
                                            seasonal_order=(param[2], D, param[3], s)).fit(disp=1)
            aic = model.aic
            print("AIC: ", aic)
            # saving best model, AIC and parameters
            if aic < best_aic:
                best_model = model
                best_aic = aic
                best_param = param
                results.append([param, model.aic])
        except Exception as error:
            continue

    result_table = pd.DataFrame(results)
    result_table.columns = ['parameters', 'aic']
    # sorting in ascending order, the lower AIC is - the better
    result_table = result_table.sort_values(by='aic', ascending=True).reset_index(drop=True)
    
    return result_table

#Create best model
best_model=sm.tsa.statespace.SARIMAX(posData, exog=exog_train, order=(p, d, q), 
                                        seasonal_order=(P, D, Q, s)).fit(disp=1)
print(best_model.summary())

#Plot to review autocorrelation and partial autocorrelation plots
tsplot(best_model.resid[24+1:], lags=52)

#Predict and review results
def mean_absolute_percentage_error(y_true, y_pred): 
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

def plotSARIMA(series, model, n_steps):
    """
        Plots model vs predicted values
        
        series - dataset with timeseries
        model - fitted SARIMA model
        n_steps - number of steps to predict in the future
        
    """
    # adding model values
    data = series.copy()
    data.columns = ['actual']
    data['arima_model'] = model.fittedvalues
    # making a shift on s+d steps, because these values were unobserved by the model
    # due to the differentiating
    data['arima_model'][:s+d] = np.NaN
    
    # forecasting on n_steps forward 
    forecast = model.predict(start = data.shape[0], end = data.shape[0]+n_steps, exog = exog_test)
    forecast = data.arima_model.append(forecast)
    # calculate error, again having shifted on s+d steps from the beginning
    error = mean_absolute_percentage_error(data['actual'][s+d:], data['arima_model'][s+d:])

    plt.figure(figsize=(16,8))
    plt.plot(m.train['guests'], label='dod_model.Train')
    plt.plot(m.test['guests'], label='Test')
    plt.plot(forecast, label='SARIMA')
    plt.legend(loc='best');
    
plotSARIMA(model_train_ts, best_model, 465)




            
#try:
#    # read the connection parameters
#    params = config()
#
#    # connect to the PostgreSQL server
#    print("Connecting to dod database...")
#    conn = psycopg2.connect(**params)
#    cur = conn.cursor()
#    print("Connection Successful!")
#except (Exception, psycopg2.DatabaseError) as error:
#    raise error
#    
#try:
#    # Run function to determine best paremeters
#    result_table = optimizeSARIMA(parameters_list, d, D, s)
#    
#    result_table.head()
#    
#    
#    p, q, P, Q = result_table.parameters[0]
#    
#    ### List of parameters to export 
#    order_parameters = [p, d, q]
#    seasonal_order = [P, D, Q, s]
#    
#except Exception as error:
#    raise error
#    
#try:
#    sql = f"""INSERT INTO %s(model_category,date,p_,d_,q_,P,D,Q,s,account_id)
#            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
#    
#    cur.execute(sql, 
#    (AsIs('model_parameters'), 
#    "sarimax",
#    datetime.datetime.now(),
#    p,d,q,P,D,Q,s,
#    1))
#
#
#    # close communication with the PostgreSQL database server
#    cur.close()
#
#    # commit the changes
#    conn.commit()
#
#except (Exception, psycopg2.DatabaseError) as error:
#    raise error
#    
##End the session
#if conn is not None:
#    print("Closing connection...")
#    conn.close()

