import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db_functions import db_connection, db_close
from config_model import start_date, end_date
import psycopg2
import pandas as pd
import numpy as np

conn, cur = db_connection()

# Query DB for our primary daily timeseries view model
def get_daily_timeseries():
    sql = f"""
        SELECT
        DATE("public"."weather"."timestamp") AS "date",
        SUM(distinct "public"."checks"."total") / 24 AS "total_sales",
        SUM("public"."checks"."guests") / 24 AS "guests",
        COUNT(distinct "public"."checks"."check_id") AS "check_count",
        ROUND(AVG(distinct "public"."weather"."temp"), 2) AS "temp",
        ROUND(MAX(distinct "public"."weather"."high_temp"), 2) AS "high_temp",
        CEILING(AVG(distinct "public"."weather"."humidity")) AS "humidity",
        CEILING(AVG(distinct "public"."weather"."weather_severity")) AS "severity"
        
        FROM "public"."checks"
        
        RIGHT JOIN "public"."weather"
        ON DATE("public"."weather"."timestamp") = DATE("public"."checks"."timestamp")
        
        WHERE DATE("public"."weather"."timestamp") BETWEEN '{start_date}' AND '{end_date}'
        
        GROUP BY DATE("public"."weather"."timestamp")
        ORDER BY "date" ASC
        """
    try:
        cur.execute(sql)
        daily_timeseries = cur.fetchall()
        return daily_timeseries

    except (Exception, psycopg2.DatabaseError) as error:
        print("get_checks error: ", error)


# Convert daily timeseries tuple into a dataframe
posData = pd.DataFrame(
    get_daily_timeseries(),
    columns=[
        "date",
        "total_sales",
        "guests",
        "check_count",
        "temp",
        "high_temp",
        "humidity",
        "severity",
    ],
    dtype=int,
)

# Set Index
posData["date"] = pd.to_datetime(posData["date"])
posData.index = posData["date"]
posData.drop("date", axis=1, inplace=True)
posData = posData.asfreq(freq="d")

# Process guests
guests_mean = posData.guests.mean(skipna=True)
posData["guests"] = posData["guests"].fillna(guests_mean)
posData["guests"].where(posData["guests"] > 10, guests_mean, inplace=True)

posData["guests_diff"] = posData.guests - posData.guests.shift(7).fillna(0)

posData["guests_diff_percent"] = (
    (posData.guests - posData.guests.shift(7))
    / ((posData.guests + posData.guests.shift(7) / 2))
).fillna(0)

posData["guests_log"] = np.log(posData.guests).fillna(0)

posData["guests_log_diff"] = posData.guests_log - posData.guests_log.shift(
    7
).fillna(0)

# Process temp
posData.temp = posData.temp.fillna(method="ffill", limit=5)
posData.temp.fillna(method="bfill", limit=5, inplace=True)

posData["temp_diff"] = posData.temp - posData.temp.shift(7).fillna(0)

posData["temp_diff_percent"] = (
    (posData.temp - posData.temp.shift(7))
    / ((posData.temp + posData.temp.shift(7) / 2))
).fillna(0)

posData["temp"] = posData["temp"].astype("int")
posData["temp_log"] = np.log(posData.temp).fillna(0)
posData.temp_log.where(posData.temp_log.values >= 0, inplace=True)

posData["temp_log_diff"] = posData.temp_log - posData.temp_log.shift(7).fillna(
    0
)

# Process severity
posData.severity.fillna(0, inplace=True)

posData["severity_diff"] = posData.severity - posData.severity.shift(7).fillna(
    0
)

# Process humidity
posData["humidity_diff"] = posData.humidity - posData.humidity.shift(7).fillna(
    0
)


missingDates = pd.date_range(start=start_date, end=end_date).difference(
    posData.index
)
if len(missingDates) > 0:
    raise Exception(
        f"{len(missingDates)} Dates are missing from the timeseries: \n{missingDates}"
    )


db_close(conn)
