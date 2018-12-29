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

#Query DB for index quotes and return a list of tuples
def get_indicies():
   sql = [
           """
           SELECT "timestamp", "index_name", "symbol", "close" 
           FROM "public"."quotes" 
           WHERE "symbol" = 'IYK'
           AND DATE("timestamp") BETWEEN '2014-3-31' AND '2015-9-30'
           """,
           """
           SELECT "timestamp", "index_name", "symbol", "close" 
           FROM "public"."quotes" 
           WHERE "symbol" = 'RHS'
           AND DATE("timestamp") BETWEEN '2014-3-31' AND '2015-9-30'
           """,
           """
           SELECT "timestamp", "index_name", "symbol", "close" 
           FROM "public"."quotes" 
           WHERE "symbol" = 'FSTA'
           AND DATE("timestamp") BETWEEN '2014-3-31' AND '2015-9-30'
           """,
           """
           SELECT "timestamp", "index_name", "symbol", "close" 
           FROM "public"."quotes" 
           WHERE "symbol" = 'VDC'
           AND DATE("timestamp") BETWEEN '2014-3-31' AND '2015-9-30'
           """,
           """
           SELECT "timestamp", "index_name", "symbol", "close" 
           FROM "public"."quotes" 
           WHERE "symbol" = 'PBJ'
           AND DATE("timestamp") BETWEEN '2014-3-31' AND '2015-9-30'
           """,
           """
           SELECT "timestamp", "index_name", "symbol", "close" 
           FROM "public"."quotes" 
           WHERE "symbol" = 'XLY'
           AND DATE("timestamp") BETWEEN '2014-3-31' AND '2015-9-30'
           """,
           """
           SELECT "timestamp", "index_name", "symbol", "close" 
           FROM "public"."quotes" 
           WHERE "symbol" = 'FXG'
           AND DATE("timestamp") BETWEEN '2014-3-31' AND '2015-9-30'
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
       print("get_checks error: ", error)


#Convert the list of index quote tuples into dataframes and assign to variables
indicies = []

for index in get_indicies():
       
   df = pandas.DataFrame(index, columns=[
                                    "date",
                                    "index_name",
                                    "symbol",
                                    "close"
                                    ])
       
   df['close'] = df['close'].astype(int)
   df['date'] = pandas.to_datetime(df['date'])
   df.index = df['date']
   df.drop('date',axis=1,inplace=True)
   
   df = df.asfreq(freq='d',method='backfill')
   
   missingDates = pandas.date_range(start = '2014-3-31', end = '2015-9-30' ).difference(df.index)

   if len(missingDates) > 0:
       raise Exception(f"{len(missingDates)} Dates are missing from the timeseries: \n{missingDates}")

   indicies.append(df)

IYK = indicies[0].copy()
RHS = indicies[1].copy()
FSTA = indicies[2].copy()
VDC = indicies[3].copy()
PBJ = indicies[4].copy()
XLY = indicies[5].copy()
FXG = indicies[6].copy() 


#End the session
if conn is not None:
    print("Closing connection...")
    conn.close()