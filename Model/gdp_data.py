import psycopg2
from psycopg2.extensions import AsIs
from psycopg2.extras import execute_values
from config import config
import pandas
from pandas import ExcelWriter
from pandas import ExcelFile
conn = None
count = 0

try:
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
except (Exception, psycopg2.DatabaseError) as error:
    raise error
finally:
    xls = ExcelFile('gdpdata.xlsx')
    df = xls.parse(xls.sheet_names[0])

    try:
        for i in df.index:
            sql = f"""INSERT INTO %s(state,gdp,date)
            VALUES(%s,%s,%s)"""
            try:
                cur.execute(sql, 
                (AsIs('food_services_gdp'), 
                df["State"][i],
                df["GDP"][i],
                df["Date"][i])
                )

                count += 1
                print("COUNT: ", count)

            except (Exception, psycopg2.DatabaseError) as error:
                raise error

    except Exception as error:
        raise error
    finally:
            try:
                print("Committing changes...")
                conn.commit()
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                raise Exception(error)
            finally:
                if conn is not None:
                    print("Closing connection.")
                    conn.close()
    