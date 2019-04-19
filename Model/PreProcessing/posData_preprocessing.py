def get_posData(account_id, start_date, end_date):
    import pandas as pd
    import numpy as np
    
    posData = get_pos_timeseries(account_id, start_date, end_date)
    
    # Convert daily timeseries tuple into a dataframe
    posData = pd.DataFrame(
        posData,
        columns=[
            "date",
            "guests",
            "total_sales",
            "check_count",
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
    
    posData["guests_squared"] = np.square(posData["guests"])
    
    # Process sales
    posData["total_sales"] = posData["total_sales"].astype("float")

    
    missingDates = pd.date_range(start=start_date, end=end_date).difference(
        posData.index
    )
    if len(missingDates) > 0:
        raise Exception(
            f"{len(missingDates)} Dates are missing from the timeseries: \n{missingDates}"
        )
    
    return posData
    
    
# Query DB for our primary daily timeseries view model
def get_pos_timeseries(account_id, start_date, end_date):
    import os, sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from db_functions import db_connection, db_close
    import psycopg2

    sql = f"""
        SELECT 
        DATE("dining_date") AS "date",
        SUM("guests") AS "guests",
        SUM("total") AS "total_sales",
        COUNT(distinct "check_id") AS "check_count"
        
        FROM checks
        WHERE DATE("dining_date") BETWEEN '{start_date}' AND '{end_date}'
        AND account_id = {account_id}
        
        GROUP BY DATE("dining_date")
        ORDER BY "date" ASC
        """
    try:
        conn, cur = db_connection()
        cur.execute(sql)
        daily_timeseries = cur.fetchall()
        db_close(conn)

        return daily_timeseries

    except (Exception, psycopg2.DatabaseError) as error:
        db_close(conn)
        raise error

if __name__ == "__main__":
    posData = get_posData(1, '2018-02-01', '2018-05-01')
    print("TEST DATA: ", posData.head())