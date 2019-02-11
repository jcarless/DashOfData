import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import psycopg2
from psycopg2.extensions import AsIs
# from config import config
from datetime import datetime, date
from db_functions import db_connection, db_close

count = 0

df = pd.read_csv(
    '/Users/jeromecarless/Documents/NYU/Capstone/DashOfData/flny_accounting_data.csv',
    usecols=["Date", "Type", "No.", "Payee", "Category", "Total", "Master Category", "Key Category"])


df["Total"] = df["Total"].str.replace(",", "")

df["Type"] = df["Type"].str.lower()
df["Category"] = df["Category"].str.lower()
df["Total"] = pd.to_numeric(df["Total"])
df["Master Category"] = df["Master Category"].str.lower()
df["Key Category"] = df["Key Category"].str.lower()
df["Master Category"][df["Master Category"] == "int. & dep."] = "interest/depreciation"

transactions = []

for i in df.index:

    transaction = {
        "account_id": 1,
        "transaction_type": df["Type"][i],
        "check_number": df["No."][i],
        "payee": df["Payee"][i],
        "transaction_category": df["Category"][i],
        "total": df["Total"][i],
        "timestamp": df["Date"][i],
        "master_category": df["Master Category"][i],
        "key_category": df["Key Category"][i]
    }

    # print("TRANSACTION===============")
    # print(transaction)

    transactions.append(transaction)

try:
    conn, cur = db_connection()

    for transaction in transactions:
        sql = f"""INSERT INTO 
        %s(account_id,
        transaction_type,
        check_number,
        master_category,
        key_category,
        payee,
        transaction_category,
        total,
        timestamp)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        try:
            # print("TRANSACTION===============")
            # print(transaction)            
            
            cur.execute(sql, 
            (AsIs('transactions'), 
            transaction["account_id"],
            transaction["transaction_type"], 
            transaction["check_number"],
            transaction["master_category"],
            transaction["key_category"],
            transaction["payee"],
            transaction["transaction_category"],
            transaction["total"],
            transaction["timestamp"]))

            count += 1
            print("COUNT: ", count)

        except (Exception, psycopg2.DatabaseError) as error:
            raise error

except Exception as error:
    raise error

try:
    print("Committing changes...")
    conn.commit()
    cur.close()
except (Exception, psycopg2.DatabaseError) as error:
    raise Exception(error)
finally:
    db_close(conn)
