# fitting a stepwise model:
from pmdarima.arima import auto_arima

def order(df):

    stepwise_fit = auto_arima(df, start_p=3, start_q=3, max_p=5, max_q=5, m=52,
                              start_P=0, seasonal=True, d=1, D=1, trace=True,
                              error_action='ignore',  # don't want to know if an order does not work
                              suppress_warnings=True,  # don't want convergence warnings
                              stepwise=True,
                              random=True,
                              n_fits=5)  # set to stepwise
    
    print("stepwise_fit: ", stepwise_fit.summary())