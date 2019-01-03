import pandas
from pandas import ExcelWriter
from pandas import ExcelFile
import psycopg2
from psycopg2.extensions import AsIs
from config import config
from datetime import datetime, date
import requests
from creds import apiKeys

data = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q=stamford&appid={apiKeys["owm"]}')
data = data.json()

count=0
conn = None

try:
    print("Connecting to PG...")
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
except (Exception, psycopg2.DatabaseError) as error:
    raise error

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
        raise error

    return

try:

    # if data["weather"][0]["main"].lower() in ("clear", "clouds"):
    #     weather_severity = 0

    # elif data["weather"][0]["main"].lower() in ("mist", "haze", "fog", "smoke", "dust", "sand", "drizzle"):
    #     weather_severity = 1

    # elif data["weather"][0]["main"].lower() in ("rain", "squall", "snow", "thunderstorm", "extreme"):
    #     weather_severity = 2
    # else:
    #     error = "Missing case: ", data["weather"][0]["main"]
    #     raise error

    # weather = {
    #     "timestamp": datetime.utcfromtimestamp(data["dt"]),
    #     "temp": round((float(data["main"]["temp"]) - 273.15) * (9.0/5) + 32, 1),
    #     "high_temp": round((float(data["main"]["temp_max"]) - 273.15) * (9.0/5) + 32, 1),
    #     "low_temp": round((float(data["main"]["temp_min"]) - 273.15) * (9.0/5) + 32, 1),
    #     "humidity": int(data["main"]["humidity"]),
    #     "wind_speed": int(data["wind"]["speed"]),
    #     "wind_direction": int(data["wind"]["deg"]),
    #     "pressure": int(data["main"]["pressure"]),
    #     "weather_severity": weather_severity,
    #     "condition_main": data["weather"][0]["main"].lower(),
    #     "condition_detail": data["weather"][0]["description"],
    #     "weather_code": int(data["weather"][0]["id"]),
    #     "city_id": int(data["id"]),
    #     "city": data["name"],
    #     "region": "new york",
    #     "country": "usa"
    # }

    weather = {
        "timestamp": datetime.utcfromtimestamp(1429488000),
        "temp": 52,
        "high_temp": 56,
        "low_temp": 47,
        "humidity": 90,
        "wind_speed": 6,
        "wind_direction": 0,
        "pressure": 30,
        "weather_severity": 0,
        "condition_main": "fog",
        "condition_detail": "fog and drizzle",
        "weather_code": 0,
        "city_id": 5128581,
        "city": "new york",
        "region": "new york",
        "country": "usa"
    }
    insert_weather(weather)
    count = count + 1
    print("RESULT: ", weather)
except Exception as error:
    raise error
finally:
    conn.commit()
    cur.close()
    if conn is not None:
        conn.close()