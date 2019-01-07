import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config_model import start_date, end_date
import psycopg2
from config import config 
import pandas

conn = None

#Create a connection to RDS
try:
    params = config()
    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
except (Exception, psycopg2.DatabaseError) as error:
    raise error

#Query DB for index quotes and return a list of tuples
def get_economy():
   sql = f"""
           SELECT "gdp", "date" FROM "public"."food_services_gdp"
           WHERE "state" = 'ny'
           AND DATE("date") BETWEEN '{start_date}' AND '{end_date}';
           """
          
   try:           
       cur.execute(sql)
       economy = cur.fetchall()
       print("Number of econ rows: ", cur.rowcount)
       return economy

   except (Exception, psycopg2.DatabaseError) as error:
       raise error

econData = pandas.DataFrame(get_economy(), columns=["gdp","date"])

econData.gdp = econData.gdp.astype(int)

econData['date'] = pandas.to_datetime(econData['date'])
econData.index = econData['date']
econData.drop('date',axis=1,inplace=True)

missingDates = pandas.date_range(start = start_date, end = end_date ).difference(econData.index)

if len(missingDates) > 0:
    raise Exception(f"{len(missingDates)} Dates are missing from the timeseries: \n{missingDates}")

#End the session
if conn is not None:
    print("Closing connection...")
    conn.close()