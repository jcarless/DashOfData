def get_weatherData(city_id, start_date, end_date):
    import pandas as pd
    import numpy as np

    weatherData = get_weather_timeseries(city_id, start_date, end_date)
    
    # Convert daily timeseries tuple into a dataframe
    weatherData = pd.DataFrame(
        weatherData,
        columns=[
            "date",
            "temp",
            "high_temp",
            "humidity",
            "severity",
        ],
        dtype=int,
    )
    
    # Set Index
    weatherData["date"] = pd.to_datetime(weatherData["date"])
    weatherData.index = weatherData["date"]
    weatherData.drop("date", axis=1, inplace=True)
    weatherData = weatherData.asfreq(freq="d")
    
    # Process temp
    weatherData.temp = weatherData.temp.fillna(method="ffill", limit=5)
    weatherData.temp.fillna(method="bfill", limit=5, inplace=True)
    
    weatherData["temp_diff"] = weatherData.temp - weatherData.temp.shift(7).fillna(0)
    
    weatherData["temp_diff_percent"] = (
        (weatherData.temp - weatherData.temp.shift(7))
        / ((weatherData.temp + weatherData.temp.shift(7) / 2))
    ).fillna(0)
    
    weatherData["temp"] = weatherData["temp"].astype("int")
    weatherData["temp_log"] = np.log(weatherData.temp).fillna(0)
    weatherData.temp_log.where(weatherData.temp_log.values >= 0, inplace=True)
    
    weatherData["temp_log_diff"] = weatherData.temp_log - weatherData.temp_log.shift(7).fillna(
        0
    )
    
    # Process severity
    weatherData.severity.fillna(0, inplace=True)
    
    weatherData["severity_diff"] = weatherData.severity - weatherData.severity.shift(7).fillna(
        0
    )
    
    # Process humidity
    weatherData["humidity_diff"] = weatherData.humidity - weatherData.humidity.shift(7).fillna(
        0
    )
    
    missingDates = pd.date_range(start=start_date, end=end_date).difference(
        weatherData.index
    )
    if len(missingDates) > 0:
        raise Exception(
            f"{len(missingDates)} Dates are missing from the timeseries: \n{missingDates}"
        )
        
    return weatherData


# Query DB for our primary daily timeseries view model
def get_weather_timeseries(city_id, start_date, end_date):
    import os, sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import psycopg2
    from db_functions import db_connection, db_close
    
    sql = f"""
        SELECT 
        DATE("timestamp") AS "date",
        ROUND(AVG("temp"), 2) AS "temp",
        ROUND(MAX("high_temp"), 2) AS "high_temp",
        CEILING(AVG("humidity")) AS "humidity",
        CEILING(AVG("weather_severity")) AS "severity"
        
        FROM weather
        WHERE DATE("timestamp") BETWEEN '{start_date}' AND '{end_date}'
        AND city_id = {city_id}
        
        GROUP BY DATE("timestamp")
        ORDER BY "date" ASC
        """
    try:
        conn, cur = db_connection()
        cur.execute(sql)
        daily_timeseries = cur.fetchall()
        db_close(conn)

        return daily_timeseries

    except (Exception, psycopg2.DatabaseError) as error:
        print("get_checks error: ", error)
        db_close(conn)


if __name__ == "__main__":
    weatherData = get_weatherData(5128581, '2018-02-01', '2018-05-01')
    print("TEST DATA: ", weatherData.head())