import pandas
from pandas import ExcelWriter
from pandas import ExcelFile
import psycopg2
from psycopg2.extensions import AsIs
from config import config
from datetime import datetime, date
error=False

# xls = ExcelFile('/Users/jeromecarless/Documents/NYU/Capstone/DashOfData/be544f711aca99913984c372ec9fd114.xls')
# df = xls.parse(xls.sheet_names[0])

df = pandas.read_csv('/Users/jeromecarless/Documents/NYU/Capstone/DashOfData/be544f711aca99913984c372ec9fd114.csv')

count=0
conn = None

try:
    print("Connecting to PG...")
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def insert_weather(weather):
    sql = f"""INSERT INTO %s(timestamp,temp,high_temp,low_temp,humidity,wind_speed,wind_direction,pressure,weather_severity,condition_main,condition_detail,weather_code,city_id,city,region,country)
    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    try:
        cur.execute(sql, 
        (AsIs('weather'), 
        weather["timestamp"], 
        weather["temp"],
        weather["high_temp"],
        weather["low_temp"],
        weather["humidity"],
        weather["wind_speed"],
        weather["wind_direction"],
        weather["pressure"],
        weather["weather_severity"],
        weather["condition_main"],
        weather["condition_detail"],
        weather["weather_code"],
        weather["city_id"],
        weather["city"],
        weather["region"],
        weather["country"])
        )

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        error=True

    return

try:
    for i in df.index:

        if df["weather_main"][i].lower() in ("clear", "clouds"):
            weather_severity = 0

        elif df["weather_main"][i].lower() in ("mist", "haze", "fog", "smoke", "dust", "sand", "drizzle"):
            weather_severity = 1

        elif df["weather_main"][i].lower() in ("rain", "squall", "snow", "thunderstorm", "extreme"):
            weather_severity = 2
        else:
            error=True
            print("Missing case: ", df["weather_main"][i])

        weather = {
            "timestamp": datetime.utcfromtimestamp(df["dt"][i]),
            "temp": round((float(df["temp"][i]) - 273.15) * (9.0/5) + 32, 1),
            "high_temp": round((float(df["temp_max"][i]) - 273.15) * (9.0/5) + 32, 1),
            "low_temp": round((float(df["temp_min"][i]) - 273.15) * (9.0/5) + 32, 1),
            "humidity": int(df["humidity"][i]),
            "wind_speed": int(df["wind_speed"][i]),
            "wind_direction": int(df["wind_deg"][i]),
            "pressure": int(df["pressure"][i]),
            "weather_severity": weather_severity,
            "condition_main": df["weather_main"][i].lower(),
            "condition_detail": df["weather_description"][i],
            "weather_code": int(df["weather_id"][i]),
            "city_id": int(df["city_id"][i]),
            "city": "new york",
            "region": "new york",
            "country": "usa"
        }
        insert_weather(weather)
        count = count + 1
        print(f"{count} rows inserted...")
except Exception as error:
    print(error)
    error=True
finally:
    if error == False:
        conn.commit()
        cur.close()
        print("SUCCESS")
    else:
        print("FAIL!")

    if conn is not None:
        conn.close()