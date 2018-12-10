import psycopg2
from config import config

# Enums
check_type_enum = "CREATE TYPE check_type_enum AS ENUM ('table', 'tab')"
status_enum = "CREATE TYPE status_enum AS ENUM ('open', 'closed')"
tax_type_enum = "CREATE TYPE tax_type_enum AS ENUM ('exclusive', 'inclusive')"
day_enum = "CREATE TYPE day_enum AS ENUM ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')"
day_of_week_enum = "CREATE TYPE day_of_week_enum AS ENUM ('0','1','2','3','4','5','6')"
month_enum = """CREATE TYPE month_enum AS ENUM (
            'january', 
            'feburary', 
            'march', 
            'april', 
            'may', 
            'june', 
            'july', 
            'august', 
            'september', 
            'october', 
            'november', 
            'december'
            )
            """
course_type_enum = """CREATE TYPE course_type_enum AS ENUM (
            'beverages',
            'first course',
            'second course',
            'third course',
            'dessert',
            'other'
            )
            """
vc_enum = "CREATE TYPE vc_enum AS ENUM ('v','c')"
vc_reason_enum = """CREATE TYPE vc_reason_enum AS ENUM (
            'long wait',
            'spillage',
            'guests changed mind',
            'server error',
            'entry error',
            'owner',
            'manager',
            'staff food',
            'other'
            )
            """

checkSchema = """
            CREATE TABLE checks (
                check_id INTEGER PRIMARY KEY, 
                check_type check_type_enum, 
                guests INTEGER NOT NULL,
                seated TIMESTAMP,
                server TEXT,
                status status_enum,
                tax_type tax_type_enum,
                total NUMERIC NOT NULL,
                day day_enum,
                day_of_week day_of_week_enum,
                month month_enum,
                year INTEGER NOT NULL
                )
            """

courseSchema = """
            CREATE TABLE courses (
                    course_id INTEGER PRIMARY KEY,
                    course_type course_type_enum,
                    total NUMERIC NOT NULL,
                    check_id INTEGER NOT NULL,
                    FOREIGN KEY (check_id) REFERENCES checks (check_id)
                )
            """

itemSchema = """
            CREATE TABLE items (
                    item_id INTEGER PRIMARY KEY,
                    item TEXT,
                    gross NUMERIC NOT NULL,
                    tax NUMERIC,
                    timestamp TIMESTAMP NOT NULL,
                    price NUMERIC NOT NULL,
                    vc vc_enum,
                    vc_note TEXT,
                    vc_reason vc_reason_enum,
                    vc_total NUMERIC,
                    course_id INTEGER REFERENCES courses (course_id),
                    check_id INTEGER REFERENCES checks (check_id)
                )
            """

indiciesSchema = """
            CREATE TABLE indicies (
                    timestamp TIMESTAMP PRIMARY KEY,
                    index_name TEXT,
                    symbol TEXT NOT NULL,
                    open NUMERIC,
                    high NUMERIC,
                    low NUMERIC,
                    close NUMERIC,
                    volume NUMERIC
                )
            """

course_check_id_index = "CREATE INDEX courses_check_fkey ON courses (check_id)"
item_check_id_index = "CREATE INDEX items_check_fkey ON items (check_id)"
item_course_id_index = "CREATE INDEX items_course_fkey ON items (course_id)"


def create_schema():
    commands = (
        "CREATE SCHEMA IF NOT EXISTS dod",
        # f"{check_type_enum}",
        # f"{status_enum}",
        # f"{tax_type_enum}",
        # f"{day_enum}",
        # f"{day_of_week_enum}",
        # f"{month_enum}",
        # f"{course_type_enum}",
        # f"{vc_enum}",
        # f"{vc_reason_enum}",
        # f"{checkSchema}",
        # f"{courseSchema}",
        # f"{itemSchema}",
        f"{indiciesSchema}",
        # f"{course_check_id_index}",
        # f"{item_check_id_index}",
        # f"{item_course_id_index}"
        )

    conn = None

    try:
        # read the connection parameters
        params = config()

        # connect to the PostgreSQL server
        print("Connecting to dod database...")
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        print("Connection Successful!")

        # create table one by one
        for command in commands:
            cur.execute(command)
            print('Command executed')

        # close communication with the PostgreSQL database server
        cur.close()

        # commit the changes
        conn.commit()
        pass
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


create_schema()