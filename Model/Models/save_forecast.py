#save_forecast(forecasts: Series - Forecasted diff values to be converted to whole values, 
#    model_name: Text - The name of the model used to produce forcasted values,  
#    account_id: Integer - The account_id of the business the model was run on,
#    parameter_id: Integer - The parameter_id of the model parameters used to run the model)

def save_forecast(forecasts, model_name, account_id, parameter_id):
    from db_functions import db_connection, db_close
    import datetime
    from psycopg2.extensions import AsIs
    from posData_preprocessing import posData
    from datetime import timedelta

    conn, cur = db_connection()
    
    last_week_index = forecasts.index - timedelta(7)
    
    forecasts = forecasts + posData["guests"].loc[last_week_index].values
            
    try:
        for forecast_date, guest_prediction in forecasts.iteritems():

            sql = f"""INSERT INTO %s(account_id, parameter_id, model, guests, sales, forecast_date, date_produced)
                    VALUES(%s,%s,%s,%s,%s,%s,%s)"""
                
            cur.execute(sql, 
                (AsIs('model_forecasts'), 
                account_id,
                parameter_id,
                model_name,
                guest_prediction,
                None,
                forecast_date,
                datetime.datetime.now()))

        conn.commit()

    except Exception as error:
        raise error
        
    finally:
        db_close(conn, cur)