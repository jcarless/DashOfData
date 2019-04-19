def get_forecasts(account_id, target_variable, model):
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
#    from dod_model import posData
#    from datetime import timedelta
    import numpy as np
    #    import os, sys
#    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#    from db_functions import db_connection, db_close
    import psycopg2

    sql = f"""
        SELECT 
        "forecast_date" AS "date",
        "guests" AS "guests"
        
        FROM "public"."model_forecasts"
        WHERE "model" = '{model}' AND "target_variable" = '{target_variable}' AND "account_id" = '{account_id}'
        ORDER BY "forecast_date" ASC
        """
    try:
        conn, cur = db_connection()
        cur.execute(sql)
        daily_timeseries = cur.fetchall()
        db_close(conn)

        return daily_timeseries

    except (Exception, psycopg2.DatabaseError) as error:
        db_close(conn)
        raise error
