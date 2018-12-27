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
           """,
           """
           SELECT "timestamp", "index_name", "symbol", "close" 
           FROM "public"."quotes" 
           WHERE "symbol" = 'RHS'
           """,
           """
           SELECT "timestamp", "index_name", "symbol", "close" 
           FROM "public"."quotes" 
           WHERE "symbol" = 'FSTA'
           """,
           """
           SELECT "timestamp", "index_name", "symbol", "close" 
           FROM "public"."quotes" 
           WHERE "symbol" = 'VDC'
           """,
           """
           SELECT "timestamp", "index_name", "symbol", "close" 
           FROM "public"."quotes" 
           WHERE "symbol" = 'FTXG'
           """,
           """
           SELECT "timestamp", "index_name", "symbol", "close" 
           FROM "public"."quotes" 
           WHERE "symbol" = 'ORG'
           """,
           """
           SELECT "timestamp", "index_name", "symbol", "close" 
           FROM "public"."quotes" 
           WHERE "symbol" = 'PBJ'
           """,
           """
           SELECT "timestamp", "index_name", "symbol", "close" 
           FROM "public"."quotes" 
           WHERE "symbol" = 'XLY'
           """,
           """
           SELECT "timestamp", "index_name", "symbol", "close" 
           FROM "public"."quotes" 
           WHERE "symbol" = 'FXG'
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
   
   indicies.append(df)

IYK = indicies[0]
RHS = indicies[1]
FSTA = indicies[2]
VDC = indicies[3]
FTXG = indicies[4]
ORG = indicies[5]
PBJ = indicies[6]
XLY = indicies[7]
FXG = indicies[8]  

#End the session
if conn is not None:
    print("Closing connection...")
    conn.close()