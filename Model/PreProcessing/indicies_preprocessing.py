import os, sys
sys.path.append(
    "/Users/jerome/Documents/NYU/Capstone/DashOfData/Model/Models"
)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append("Model/Models")
from lags import lags
from db_functions import db_connection, db_close
from config_model import start_date, end_date
import psycopg2
import pandas

conn, cur = db_connection()

#Query DB for index quotes and return a list of tuples
def get_indicies():
   sql = [
           f"""
           SELECT "timestamp", "index_name", "symbol", "close" 
           FROM "public"."quotes" 
           WHERE "symbol" = 'IYK'
           AND DATE("timestamp") BETWEEN '{start_date}' AND '{end_date}'
           """,
           f"""
           SELECT "timestamp", "index_name", "symbol", "close" 
           FROM "public"."quotes" 
           WHERE "symbol" = 'RHS'
           AND DATE("timestamp") BETWEEN '{start_date}' AND '{end_date}'
           """,
           f"""
           SELECT "timestamp", "index_name", "symbol", "close" 
           FROM "public"."quotes" 
           WHERE "symbol" = 'FSTA'
           AND DATE("timestamp") BETWEEN '{start_date}' AND '{end_date}'
           """,
           f"""
           SELECT "timestamp", "index_name", "symbol", "close" 
           FROM "public"."quotes" 
           WHERE "symbol" = 'VDC'
           AND DATE("timestamp") BETWEEN '{start_date}' AND '{end_date}'
           """,
           f"""
           SELECT "timestamp", "index_name", "symbol", "close" 
           FROM "public"."quotes" 
           WHERE "symbol" = 'PBJ'
           AND DATE("timestamp") BETWEEN '{start_date}' AND '{end_date}'
           """,
           f"""
           SELECT "timestamp", "index_name", "symbol", "close" 
           FROM "public"."quotes" 
           WHERE "symbol" = 'XLY'
           AND DATE("timestamp") BETWEEN '{start_date}' AND '{end_date}'
           """,
           f"""
           SELECT "timestamp", "index_name", "symbol", "close" 
           FROM "public"."quotes" 
           WHERE "symbol" = 'FXG'
           AND DATE("timestamp") BETWEEN '{start_date}' AND '{end_date}'
           """,
           f"""
           SELECT "timestamp", "index_name", "symbol", "close" 
           FROM "public"."quotes" 
           WHERE "symbol" = 'QQQ'
           AND DATE("timestamp") BETWEEN '{start_date}' AND '{end_date}'
           """
          ]
           
   try:
       quote_lists = []
       for sql in sql:
           
           cur.execute(sql)
           index = cur.fetchall()
           quote_lists.append(index)
           
       return quote_lists

   except (Exception, psycopg2.DatabaseError) as error:
       raise error


#Convert the list of index quote tuples into dataframes and assign to variables
indicies = []

for index in get_indicies():
       
   df = pandas.DataFrame(index, columns=[
                                    "date",
                                    "index_name",
                                    "symbol",
                                    "close"
                                    ],
                                 dtype=int)
       
   df.date = pandas.to_datetime(df.date)
   df.index = df.date
   df.drop('date',axis=1,inplace=True)
   
   df = df.asfreq(freq='d', method='backfill')
   
   missingDates = pandas.date_range(start = start_date, end = end_date ).difference(df.index)

   if len(missingDates) > 0:
       raise Exception(f"{len(missingDates)} Dates are missing from the timeseries: \n{missingDates}")

   indicies.append(df)

for i in range(0, len(indicies)):
    fund = indicies[i]
    name = fund["symbol"][0]
    fund[f'{name}_close_diff'] = fund['close'] - fund['close'].shift(7)
    fund[f'{name}_close_diff'].fillna(0, inplace=True)
    
    lag = lags(fund, name)
    lag7 = lag[f'{name}_close_lag_7'].copy()
    
    fund[f'{name}_close_diff_lag7'] = lag7 - lag7.shift(7)
    fund[f'{name}_close_diff_lag7'].fillna(0, inplace=True)
    
IYK = indicies[0].copy()
RHS = indicies[1].copy()
FSTA = indicies[2].copy()
VDC = indicies[3].copy()
PBJ = indicies[4].copy()
XLY = indicies[5].copy()
FXG = indicies[6].copy() 
QQQ = indicies[7].copy() 

db_close(conn)