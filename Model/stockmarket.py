from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import psycopg2
from psycopg2.extensions import AsIs
from config import config

symbol="XLY"
ts = TimeSeries(key='7WPQAG2NRC8PLFIZ', output_format='pandas')
# data, meta_data = ts.get_daily(symbol='NRN', outputsize='full')
data, meta_data = ts.get_daily(symbol=symbol, outputsize='full')
df = data.tail(5)

conn = None


try:
    # read database configuration
    params = config()
    # connect to the PostgreSQL database
    conn = psycopg2.connect(**params)
    # create a new cursor
    cur = conn.cursor()
except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def insert_index(stock_index):
    sql = f"""INSERT INTO %s(timestamp,index_name,symbol,open,high,low,close,volume)
    VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"""
    try:
        # execute the INSERT statement
        cur.execute(sql, 
        (AsIs('indicies'), 
        stock_index["timestamp"], 
        stock_index["index_name"],
        stock_index["symbol"],
        stock_index["open"],
        stock_index["high"],
        stock_index["low"],
        stock_index["close"],
        stock_index["volume"])
        )
        # get the generated id back
        # timestamp = cur.fetchone()[0]

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
 
    return

try:
    for index, row in df.iterrows():
        stock_index = {
            "timestamp": index,
            "index_name": "test",
            "symbol": symbol,
            "open": row[0],
            "high": row[1],
            "low": row[2],
            "close": row[3],
            "volume": row[4]
        }
        # print(stock_index)
        insert_index(stock_index)
except Exception as error:
    print(error)
finally:
    # commit the changes to the database
    conn.commit()
    # close communication with the database
    cur.close()

    if conn is not None:
        conn.close()
