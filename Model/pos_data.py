import psycopg2
from psycopg2.extensions import AsIs
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
errors=[]
fail=False

items = []
courses = []
checks = []
courses_with_ids = []
checks_with_ids = []

def searchChecks(checkNumber, timestamp, gross, calculate, newCheckNumber):
    if calculate == 0:
        # print("checkNumber: ", checkNumber)
        # print("courseType: ", courseType)
        for c in checks_with_ids:
            if c['check_id_temp'] == checkNumber and c['timestamp'] == timestamp:
                return c

    else:
        for c in checks:
            if c['check_id_temp'] == checkNumber and c['timestamp'] == timestamp:
                if calculate == 1:
                    c["total"] = round(c["total"] + float(gross), 2)
                    return False                    
                if calculate == 2:
                    c["check_id"] = newCheckNumber
                    checks_with_ids.append(c)
                    return c
    return True

def searchCourses(checkNumber, timestamp, courseType, gross, calculate, course_id):
    if calculate == 0:
        # print("checkNumber: ", checkNumber)
        # print("courseType: ", courseType)
        for c in courses_with_ids:
            if c['check_id_temp'] == checkNumber and c["course_type"] == courseType and c['timestamp'] == timestamp:
                # print("Course with id again: ", c)
                return c
        print("YOU SHOULD HAVE FOUND A COURSE!")
        print("================================")
        print("================================")
        print("================================")
        print("================================")
        print("================================")

    else:
        for c in courses:
            if c['check_id_temp'] == checkNumber and c["course_type"] == courseType:
                if calculate == 1:
                    c["total"] = round(c["total"] + float(gross), 2)
                    return False
                if calculate == 2:
                    c["course_id"] = course_id
                    # print("Course added to array: ", c)
                    courses_with_ids.append(c)
                    return False
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
    # print("COURSE: ", item["course_type"])
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

xls = ExcelFile('nydata_7.xlsx')
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
            # print("UNKNOWN COURSE TYPE CONVERTED TO OTHER: ", df["Course"][i])
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
        "item": df["Item"][i],
        "gross": round(float(df["Gross"][i]), 2),
        "tax": round(float(str(df["Item Tax"][i]).replace("$", "")),2) if type(df["Item Tax"][i]).__name__ == "str" else 0.0,
        "timestamp": df["Seated"][i],
        "price": round(float(df["Price"][i].replace("$", "").replace(",", "")), 2),
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
    print("CONNECTION ERROR: ", error)
finally:
    for check in checks:
        try:
            check["check_id"] = insert_check(check)
            searchChecks(check["check_id_temp"], check["timestamp"], "", 2, check["check_id"])
            checksInsertedCount = checksInsertedCount + 1
            print("checksInsertedCount: ", checksInsertedCount)
        except Exception as error:
            fail=True
            print("CHECK ERROR: ", error)
            print(check)
            errors.append(error)

    for course in courses:
        try:
            check = searchChecks(course["check_id_temp"], course["timestamp"], "", 0, "")
            course["check_id"] = check["check_id"]
            course_id = insert_course(course)
            searchCourses(course["check_id_temp"], course["timestamp"], course["course_type"], "", 2, course_id)
            coursesInsertedCount = coursesInsertedCount + 1
            print("coursesInsertedCount: ", coursesInsertedCount)
        except Exception as error:
            fail=True
            print("COURSE ERROR: ", error) 
            print(course)
            errors.append(error)  

    for item in items:
        try:
            courseMatch = searchCourses(item["check_id_temp"], item["timestamp"], item["course_type"], "", 0, 0)
            item["course_id"] = courseMatch["course_id"]
            item["check_id"] = courseMatch["check_id"]
            insert_item(item)
            itemsInsertedCount = itemsInsertedCount + 1
            print("itemsInsertedCount: ", itemsInsertedCount)
        except Exception as error:
            fail=True
            print("ITEM ERROR: ", error)  
            print(item)
            errors.append(error)

    try:
        if fail == False:
            conn.commit()
            cur.close()
            print("SUCCESS")
            print("ERRORS: ", errors)
            print("NUMBER OF ERRORS: ", len(errors))
            print("CHECKS: ", len(checks))
            print("COURSES: ", len(courses))
            print("ITEMS: ", len(items))
        else:
            print("FAIL")
            print("Data not saved!")
            print("ERRORS: ", errors)
            print("NUMBER OF ERRORS: ", len(errors))

    except (Exception, psycopg2.DatabaseError) as error:
        print("Commit/Close error: ", error)
    finally:
        if conn is not None:
            conn.close()