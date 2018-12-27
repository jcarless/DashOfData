import psycopg2
from config import config 
import pandas
import pandas.io.sql as psql
import numpy as np
conn = None

#Create a connection to RDS
try:
    params = config()
    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
except (Exception, psycopg2.DatabaseError) as error:
    print("CONNECTION ERROR: ", error)

#Query DB for our primary daily timeseries view model
def get_daily_timeseries():
    sql = """
        SELECT 
        DATE("public"."weather"."timestamp") AS "date", 
        SUM(distinct "public"."checks"."total") AS "total_sales", 
        SUM("public"."checks"."guests") AS "guests",
        COUNT(distinct "public"."checks"."check_id") AS "check_count",
        ROUND(AVG(distinct "public"."weather"."temp"), 2) AS "temp",
        CEILING(AVG(distinct "public"."weather"."humidity")) AS "humidity",
        CEILING(AVG(distinct "public"."weather"."weather_severity")) AS "severity"
        
        FROM "public"."checks"
        
        RIGHT JOIN "public"."weather" 
        ON DATE("public"."weather"."timestamp") = DATE("public"."checks"."timestamp")
        AND EXTRACT(HOUR FROM "public"."weather"."timestamp") = EXTRACT(HOUR FROM "public"."checks"."timestamp")
        
        WHERE DATE("public"."weather"."timestamp") BETWEEN '2014-2-1' AND '2015-9-30'
        
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


posData.total_sales = posData.total_sales.astype(int)
posData.temp = posData.temp.astype(int)
posData.humidity = posData.humidity.astype(int)
posData.severity = posData.severity.astype(int)

posData["guests"] = posData["guests"].mask(posData["guests"] == 0, 0.0001)

posData['date'] = pandas.to_datetime(posData['date'])
posData.index = posData['date']
posData.drop('date',axis=1,inplace=True)


#End the session
if conn is not None:
    print("Closing connection...")
    conn.close()