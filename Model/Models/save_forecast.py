#save_forecast(
#    forecasts: Series - Forecasted diff values to be converted to whole values,
#    target_variable: Text - The target variable used for the model
#    model_name: Text - The name of the model used to produce forcasted values,  
#    account_id: Integer - The account_id of the business the model was run on,
#    parameter_id: Integer - The parameter_id of the model parameters used to run the model)

def save_forecast(forecasts, 
                  target_variable, 
                  model_name, 
                  account_id, 
                  parameter_id=None):
#    import sys
#    import os
#
#    sys.path.append(
#        "/Users/jerome/Documents/NYU/Capstone/DashOfData/Model/PreProcessing"
#    )
#    sys.path.append("Model/Models")
#    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from db_functions import db_connection, db_close
    import datetime
    from psycopg2.extensions import AsIs
    from dod_model import posData
    from datetime import timedelta
    import numpy as np
    
    print("********VAR NAME**********: ", target_variable)

    conn, cur = db_connection()
    
    last_week_index = forecasts.index - timedelta(7)
                      
    try:
        if target_variable == "guests_log_diff":
            forecasts = forecasts + posData["guests_log"].loc[last_week_index].values
            forecasts = np.exp(forecasts)
        
        if target_variable == "guests_diff":
            forecasts = forecasts + posData["guests"].loc[last_week_index].values
        
        if target_variable == "guests_log_diff_val":
            forecasts = forecasts + posData["guests_log"].loc[last_week_index].values
            forecasts = np.exp(forecasts)
            
#        print("*****ACTUAL*****: ", posData["guests"].loc[last_week_index].values)
#        print("*****FORECAST*****: ", forecasts)
            
        for forecast_date, guest_prediction in forecasts.iteritems():

            sql = f"""INSERT INTO %s(account_id, 
            parameter_id, 
            model, 
            guests, 
            sales, 
            forecast_date, 
            date_produced,
            target_variable)
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"""
                
            cur.execute(sql, 
                (AsIs('model_forecasts'), 
                account_id,
                parameter_id,
                model_name,
                guest_prediction,
                None,
                forecast_date,
                datetime.datetime.now(),
                target_variable))

        conn.commit()

    except Exception as error:
        raise error
        
    else:
        db_close(conn, cur)