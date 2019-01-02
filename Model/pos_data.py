import psycopg2
from psycopg2.extensions import AsIs
from psycopg2.extras import execute_values
from config import config
import pandas
from pandas import ExcelWriter
from pandas import ExcelFile
import uuid
import math
conn = None

count = 0
checksInsertedCount = 0
itemsInsertedCount = 0
coursesInsertedCount = 0

items = []
courses = []
checks = []

def setItemIds():
    i = 0
    while i < len(items):
        courseMatch = searchCourses(items[i]["check_id_temp"], items[i]["timestamp"], items[i]["course_type"], "", 0, 0)

        items[i]["check_id"] = courseMatch["check_id"]
        items[i]["course_id"] = courseMatch["course_id"]

        del items[i]["course_type"]
        del items[i]["check_id_temp"]

        items[i] = tuple(items[i].values())

        i += 1

def searchChecks(checkNumber, timestamp, gross, calculate, newCheckNumber):
    i = 0
    if calculate == 0:
        while i < len(courses):
            if courses[i]['check_id_temp'] == checkNumber and courses[i]['timestamp'] == timestamp:
                return courses[i]
            i+=1

    else:
        while i < len(courses):
            if courses[i]['check_id_temp'] == checkNumber and courses[i]['timestamp'] == timestamp:
                if calculate == 1:
                    courses[i]["total"] = round(courses[i]["total"] + float(gross), 2)
                    return False                    
                if calculate == 2:
                    courses[i]["check_id"] = newCheckNumber
                    return courses[i]
            i+=1
    return True

def searchCourses(checkNumber, timestamp, courseType, gross, calculate, course_id):
    i = 0
    if calculate == 0:
        while i < len(courses):
            if courses[i]['check_id_temp'] == checkNumber and courses[i]["course_type"] == courseType and courses[i]['timestamp'] == timestamp:
                return courses[i]
            i += 1
        raise Exception("YOU SHOULD HAVE FOUND A COURSE!")

    else:
        while i < len(courses):
            if courses[i]['check_id_temp'] == checkNumber and courses[i]["course_type"] == courseType:
                if calculate == 1:
                    courses[i]["total"] = round(courses[i]["total"] + float(gross), 2)
                    return False
                if calculate == 2:
                    courses[i]["course_id"] = course_id
                    return False
            i+=1
    return True

def insert_item(item):
    sql = f"""INSERT INTO %s(item,gross,tax,timestamp,price,vc,vc_note,vc_reason,vc_total,check_id,course_id)
    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    try:
        cur.execute(sql, 
        (AsIs('items'), 
        item["item"], 
        item["gross"],
        item["tax"],
        item["timestamp"],
        item["price"],
        item["vc"],
        item["vc_note"],
        item["vc_reason"],
        item["vc_total"],
        item["check_id"],
        item["course_id"])
        )

    except (Exception, psycopg2.DatabaseError) as error:
        print("insert_item error: ", error)

    return

def insert_check(item):
    sql = f"""INSERT INTO %s(check_type,guests,timestamp,server,status,tax_type,total,day,day_of_week,month,year)
    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING check_id"""
    try:
        cur.execute(sql, 
        (AsIs('checks'), 
        item["check_type"],
        item["guests"],
        item["timestamp"],
        item["server"],
        item["status"],
        item["tax_type"],
        item["total"],
        item["day"],
        item["day_of_week"],
        item["month"],
        item["year"])
        )

    except (Exception, psycopg2.DatabaseError) as error:
        print("insert_check error: ", error)

    return cur.fetchone()[0]

def insert_course(item):
    sql = f"""INSERT INTO %s(check_id,course_type,total)
    VALUES(%s,%s,%s) RETURNING course_id"""
    try:
        cur.execute(sql, 
        (AsIs('courses'), 
        item["check_id"], 
        item["course_type"],
        item["total"])
        )

    except (Exception, psycopg2.DatabaseError) as error:
        print("insert_course error: ", error)

    return cur.fetchone()[0]

xls = ExcelFile('nydata-3.xlsx')
df = xls.parse(xls.sheet_names[0])

for i in df.index:

    if math.isnan(df["Gross"][i]):
        df["Gross"][i] = 0.0

    if type(df["Course"][i]).__name__ != "str":
        df["Course"][i] = "other"
    else:
        df["Course"][i] = df["Course"][i].lower()
        if df["Course"][i] == "1st course":
            df["Course"][i] = "first course"
        elif df["Course"][i] == "2nd course":
            df["Course"][i] = "second course"
        elif df["Course"][i] == "3rd course":
            df["Course"][i] = "third course"
        elif df["Course"][i] == "beverages":
            pass
        elif df["Course"][i] == "dessert":
            pass
        else:
            df["Course"][i] = "other"

    newCheck = searchChecks(df["Check_Number"][i], df["Seated"][i], df["Gross"][i], 1, "")
    newCourse = searchCourses(df["Check_Number"][i],df["Seated"][i], df["Course"][i], df["Gross"][i], 1, 0)

    if newCheck == True:

        if df["Check_Type"][i].lower() == "to go":
            df["Check_Type"][i] = "takeout"  
        
        check = {
            "check_id_temp": int(df["Check_Number"][i]),
            "check_type": str(df["Check_Type"][i].lower()),
            "guests": int(df["Guests"][i]),
            "timestamp": df["Seated"][i],
            "server": df["Server"][i],
            "status": df["Status"][i].lower(),
            "tax_type": df["Tax Type"][i].lower(),
            "total": df["Gross"][i],
            "day": df["Day"][i],
            "day_of_week": str(df["Day of the Week"][i]),
            "month": df["Seated"][i].strftime("%B").lower(),
            "year": int(df["Seated"][i].year)
        }
        checks.append(check)

    if newCourse == True:

        course = {
            "check_id_temp": int(df["Check_Number"][i]),
            "course_type": df["Course"][i],
            "total": round(float(df["Gross"][i]),2),
            "timestamp": df["Seated"][i]
        }
        courses.append(course)

    item = {
        "item": df["Item"][i] if type(df["Item"][i]).__name__ == "str" else None,
        "gross": round(float(df["Gross"][i]), 2),
        "tax": round(float(str(df["Item Tax"][i]).replace("$", "")),2) if type(df["Item Tax"][i]).__name__ == "str" else 0.0,
        "timestamp": df["Seated"][i],
        "price": round(float(str(df["Price"][i]).replace("$", "").replace(",", "")), 2),
        "vc": df["VC"][i] if type(df["VC"]).__name__ == "str" else None,
        "vc_note": df["VC_Note"][i],
        "vc_reason": df["VC_Reason"][i] if type(df["VC"]).__name__ == "str" else None,
        "vc_total": round(float(str(df["VC_Total"][i]).replace("$", "").replace(",", "")), 2) if type(df["VC_Total"][i]).__name__ == "str" else 0.0,
        "check_id": int(df["Check_Number"][i]),
        "check_id_temp": int(df["Check_Number"][i]),
        "course_type": df["Course"][i]
    }
    items.append(item)
    count = count + 1
    print("COUNT: ", count)

try:
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
except (Exception, psycopg2.DatabaseError) as error:
    raise error
finally:
    try:
        try:
            for check in checks:
                check["check_id"] = insert_check(check)
                searchChecks(check["check_id_temp"], check["timestamp"], "", 2, check["check_id"])
                checksInsertedCount = checksInsertedCount + 1
                print("checksInsertedCount: ", checksInsertedCount)
        except Exception as error:
            print("CHECK ERROR: ", check) 
            raise error

        try:
            for course in courses:
                check = searchChecks(course["check_id_temp"], course["timestamp"], "", 0, "")
                course["check_id"] = check["check_id"]
                course_id = insert_course(course)
                searchCourses(course["check_id_temp"], course["timestamp"], course["course_type"], "", 2, course_id)
                coursesInsertedCount = coursesInsertedCount + 1
                print("coursesInsertedCount: ", coursesInsertedCount)
        except Exception as error:
            print("COURSE ERROR: ", course) 
            raise error

        try:
            setItemIds()
            execute_values(cur,
            """INSERT INTO items (item,
            gross,
            tax,
            timestamp,
            price,
            vc,
            vc_note,
            vc_reason,
            vc_total,
            check_id,
            course_id) VALUES %s""",
            items)

        except Exception as error:
            print("ITEM ERROR: ", item)
            raise error

        try:
            print("Committing changes...")
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            raise Exception(error)

    except Exception as error:
        raise error

    finally:
        if conn is not None:
            print("Closing connection.")
            conn.close()