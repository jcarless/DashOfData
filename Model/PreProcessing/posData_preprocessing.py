import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db_functions import db_connection, db_close
from config_model import start_date, end_date
import psycopg2
from config import config 
import pandas
import pandas.io.sql as psql
import numpy as np

conn, cur = db_connection()


#Query DB for our primary daily timeseries view model
def get_daily_timeseries():
    sql = f"""
        SELECT 
        DATE("public"."weather"."timestamp") AS "date", 
        SUM(distinct "public"."checks"."total") AS "total_sales", 
        SUM("public"."checks"."guests") AS "guests",
        COUNT(distinct "public"."checks"."check_id") AS "check_count",
        ROUND(AVG(distinct "public"."weather"."temp"), 2) AS "temp",
        ROUND(MAX(distinct "public"."weather"."high_temp"), 2) AS "high_temp",
        CEILING(AVG(distinct "public"."weather"."humidity")) AS "humidity",
        CEILING(AVG(distinct "public"."weather"."weather_severity")) AS "severity"
        
        FROM "public"."checks"
        
        RIGHT JOIN "public"."weather" 
        ON DATE("public"."weather"."timestamp") = DATE("public"."checks"."timestamp")
        
        WHERE DATE("public"."weather"."timestamp") BETWEEN '{start_date}' AND '{end_date}'
        
        GROUP BY DATE("public"."weather"."timestamp")
        ORDER BY "date" ASC
        """
    try:
        cur.execute(sql)
        daily_timeseries = cur.fetchall()
        print("Number of daily_timeseries: ", cur.rowcount)
        return daily_timeseries

    except (Exception, psycopg2.DatabaseError) as error:
        print("get_checks error: ", error)
        
        
#Convert daily timeseries tuple into a dataframe
posData = pandas.DataFrame(get_daily_timeseries(), 
                           columns=[
                                 "date",
                                 "total_sales",
                                 "guests",
                                 "check_count",
                                 "temp",
                                 "high_temp",
                                 "humidity",
                                 "severity"
                                 ])
    
#convert Quantity feature from float to integer
posData[~posData.isin([np.nan, np.inf, -np.inf]).any(1)]
posData.mask(posData.eq('None')).dropna()

posData["guests"] = posData["guests"].fillna(0)
posData["total_sales"] = posData["total_sales"].fillna(0)
posData["humidity"] = posData["humidity"].fillna(0)
posData["severity"] = posData["severity"].fillna(0)
posData["temp"] = posData["temp"].fillna(0)
posData["high_temp"] = posData["temp"].fillna(0)

posData.total_sales = posData.total_sales.astype(int)
posData.temp = posData.temp.astype(int)
posData.humidity = posData.humidity.astype(int)
posData.severity = posData.severity.astype(int)
posData.high_temp = posData.high_temp.astype(int)


posData["guests"] = posData["guests"].mask(posData["guests"] == 0, 0.0001)

posData['date'] = pandas.to_datetime(posData['date'])
posData.index = posData['date']
posData.drop('date',axis=1,inplace=True)
posData = posData.asfreq(freq='d')

#Guests transform
posData['guests_log'] = np.log(posData['guests'])
posData['guests_log'][posData['guests_log'] < 0] = 0
posData['guests_log_diff'] = posData['guests_log'] - posData['guests_log'].shift(7)
posData['guests_log_diff'] = posData['guests_log_diff'].dropna()
posData["guests_log_diff"][0] = 0
posData["guests_log_diff"][1] = 0
posData["guests_log_diff"][2] = 0
posData["guests_log_diff"][3] = 0
posData["guests_log_diff"][4] = 0
posData["guests_log_diff"][5] = 0
posData["guests_log_diff"][6] = 0


posData['guests_diff'] = posData['guests'] - posData['guests'].shift(7)
posData['guests_diff'] = posData['guests_diff'].dropna()
posData["guests_diff"][0] = 0
posData["guests_diff"][1] = 0
posData["guests_diff"][2] = 0
posData["guests_diff"][3] = 0
posData["guests_diff"][4] = 0
posData["guests_diff"][5] = 0
posData["guests_diff"][6] = 0

posData['guests_diff_percent'] = ((posData['guests'] - posData['guests'].shift(7)) 
    / ((posData['guests'] + posData['guests'].shift(7) 
    / 2)))
posData['guests_diff_percent'] = posData['guests_diff_percent'].dropna()
posData["guests_diff_percent"][0] = 0
posData["guests_diff_percent"][1] = 0
posData["guests_diff_percent"][2] = 0
posData["guests_diff_percent"][3] = 0
posData["guests_diff_percent"][4] = 0
posData["guests_diff_percent"][5] = 0
posData["guests_diff_percent"][6] = 0

#Temp transform
posData['temp_log'] = np.log(posData['temp'])
posData['temp_log'][posData['temp_log'] < 0] = 0
posData['temp_log_diff'] = posData['temp_log'] - posData['temp_log'].shift(7)
posData['temp_log_diff'] = posData['temp_log_diff'].dropna()
posData["temp_log_diff"][0] = 0
posData["temp_log_diff"][1] = 0
posData["temp_log_diff"][2] = 0
posData["temp_log_diff"][3] = 0
posData["temp_log_diff"][4] = 0
posData["temp_log_diff"][5] = 0
posData["temp_log_diff"][6] = 0

posData['temp_diff'] = posData['temp'] - posData['temp'].shift(7)
posData['temp_diff'] = posData['temp_diff'].dropna()
posData["temp_diff"][0] = 0
posData["temp_diff"][1] = 0
posData["temp_diff"][2] = 0
posData["temp_diff"][3] = 0
posData["temp_diff"][4] = 0
posData["temp_diff"][5] = 0
posData["temp_diff"][6] = 0

posData['temp_diff_percent'] = ((posData['temp'] - posData['temp'].shift(7)) 
    / ((posData['temp'] + posData['temp'].shift(7) 
    / 2)))
posData['temp_diff_percent'] = posData['temp_diff_percent'].dropna()
posData["temp_diff_percent"][0] = 0
posData["temp_diff_percent"][1] = 0
posData["temp_diff_percent"][2] = 0
posData["temp_diff_percent"][3] = 0
posData["temp_diff_percent"][4] = 0
posData["temp_diff_percent"][5] = 0
posData["temp_diff_percent"][6] = 0

missingDates = pandas.date_range(start = start_date, end = end_date ).difference(posData.index)

if len(missingDates) > 0:
    raise Exception(f"{len(missingDates)} Dates are missing from the timeseries: \n{missingDates}")


db_close(conn)