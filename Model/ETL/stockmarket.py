import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import psycopg2
from alpha_vantage.timeseries import TimeSeries
from psycopg2.extensions import AsIs
from config import config
from creds import apiKeys

print("Getting data...")
count = 0
symbols = [
    {
    "symbol": "QQQ",
    "index_name": "PowerShares QQQ Trust, Series 1"  
    },
    {
    "symbol": "RYDAX",
    "index_name": "Rydex Dow Jones Industrial Average Fund Class A"  
    },
    # {
    # "symbol": "IYK",
    # "index_name": "iShares U.S. Consumer Goods ETF"  
    # },
    # {
    # "symbol": "RHS",
    # "index_name": "Invesco S&P 500® Equal Weight Consumer Staples ETF"  
    # },    {
    # "symbol": "FSTA",
    # "index_name": "Fidelity MSCI Consumer Staples Index ETF"  
    # },    
    # {
    # "symbol": "VDC",
    # "index_name": "Vanguard Consumer Staples ETF"  
    # },    
    # {
    # "symbol": "FTXG",
    # "index_name": "First Trust Nasdaq Food & Beverage ETF"  
    # },    
    # {
    # "symbol": "ORG",
    # "index_name": "Organics ETF"  
    # },    
    # {
    # "symbol": "PBJ",
    # "index_name": "Invesco Dynamic Food & Beverage ETF"  
    # },    
    # {
    # "symbol": "XLY",
    # "index_name": "Consumer Discret Sel Sect SPDR ETF"  
    # },
    # {
    # "symbol": "FXG",
    # "index_name": "First Trust Consumer Staples AlphaDEX Fund"  
    # }
]

for symbol in symbols:

    ts = TimeSeries(key=apiKeys["alpha_vantage"], output_format='pandas')
    data, meta_data = ts.get_daily(symbol=symbol["symbol"], outputsize='full')
    df = data

    conn = None

    try:
        print("Connecting to PG...")
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
    except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def insert_index(stock_index):
        sql = f"""INSERT INTO %s(timestamp,index_name,symbol,open,high,low,close,volume)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"""
        try:
            cur.execute(sql, 
            (AsIs('quotes'), 
            stock_index["timestamp"], 
            stock_index["index_name"],
            stock_index["symbol"],
            stock_index["open"],
            stock_index["high"],
            stock_index["low"],
            stock_index["close"],
            stock_index["volume"])
            )

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    
        return

    try:
        for index, row in df.iterrows():
            stock_index = {
                "timestamp": index,
                "index_name": symbol["index_name"],
                "symbol": symbol["symbol"],
                "open": row[0],
                "high": row[1],
                "low": row[2],
                "close": row[3],
                "volume": row[4]
            }
            insert_index(stock_index)
            count = count + 1
            print(f"{count} row inserted...")
    except Exception as error:
        raise error
    finally:
        conn.commit()
        cur.close()

        if conn is not None:
            conn.close()
