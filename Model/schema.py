import psycopg2
from config import config

# Enums
account_type_enum = """CREATE TYPE account_type_enum AS ENUM (
            'restaurant'
            )
            """
model_category_enum = """CREATE TYPE model_category_enum AS ENUM (
            'var',
            'svar',
            'mlp',
            'lstm',
            'arima',
            'sarima',
            'sarimax',
            'holtwinter'
            )
            """
condition_main_enum = "CREATE TYPE condition_main_enum AS ENUM ('clear', 'clouds', 'mist', 'haze', 'fog', 'smoke', 'dust', 'sand', 'drizzle', 'rain', 'squall', 'snow', 'thunderstorm', 'extreme')"
check_type_enum = "CREATE TYPE check_type_enum AS ENUM ('table', 'tab', 'takeout')"
status_enum = "CREATE TYPE status_enum AS ENUM ('open', 'closed')"
tax_type_enum = "CREATE TYPE tax_type_enum AS ENUM ('exclusive', 'inclusive')"
day_enum = "CREATE TYPE day_enum AS ENUM ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')"
day_of_week_enum = "CREATE TYPE day_of_week_enum AS ENUM ('0','1','2','3','4','5','6')"
month_enum = """CREATE TYPE month_enum AS ENUM (
            'january', 
            'february', 
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
state_enum = """CREATE TYPE state_enum AS ENUM (
            'ny',
            'ct'
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
transaction_type_enum = """CREATE TYPE transaction_type_enum AS ENUM (
            'bill',
            'bill payment (check)',
            'bill payment (credit card)',
            'check',
            'credit card credit',
            'expense',
            'vendor credit'
            )
            """

checkSchema = """
            CREATE TABLE checks (
                check_id serial PRIMARY KEY, 
                check_type check_type_enum, 
                guests INTEGER NOT NULL,
                timestamp TIMESTAMP,
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
                    course_id serial PRIMARY KEY,
                    course_type course_type_enum,
                    total NUMERIC NOT NULL,
                    check_id INTEGER NOT NULL,
                    FOREIGN KEY (check_id) REFERENCES checks (check_id)
                )
            """

itemSchema = """
            CREATE TABLE items (
                    item_id serial PRIMARY KEY,
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

quotesSchema = """
            CREATE TABLE quotes (
                    quote_id serial PRIMARY KEY,
                    timestamp TIMESTAMP,
                    index_name TEXT,
                    symbol TEXT NOT NULL,
                    open NUMERIC,
                    high NUMERIC,
                    low NUMERIC,
                    close NUMERIC,
                    volume NUMERIC
                )
            """

weatherSchema = """
CREATE TABLE weather (
    weather_id serial PRIMARY KEY,
    timestamp TIMESTAMP,
    temp NUMERIC NOT NULL,
    high_temp NUMERIC,
    low_temp NUMERIC,
    humidity INTEGER,
    wind_speed INTEGER,
    wind_direction INTEGER,
    pressure INTEGER,
    weather_severity INTEGER NOT NULL,
    condition_main condition_main_enum NOT NULL,
    condition_detail TEXT,
    weather_code INTEGER,
    city_id INTEGER,
    city TEXT,
    region TEXT,
    country TEXT
    )
"""

food_services_gdp_Schema = """
CREATE TABLE food_services_gdp (
    gdp_id serial PRIMARY KEY,
    state state_enum NOT NULL,
    gdp NUMERIC NOT NULL,
    date TIMESTAMP NOT NULL
    )
"""

accounts_Schema = """
CREATE TABLE accounts (
    account_id serial PRIMARY KEY,
    name TEXT,
    address TEXT NOT NULL,
    city TEXT NOT NULL,
    state state_enum NOT NULL,
    zip TEXT,
    type account_type_enum
    )
"""

model_parameters_Schema = """
CREATE TABLE model_parameters (
    parameter_id serial PRIMARY KEY,
    model_category model_category_enum NOT NULL,
    date TIMESTAMP NOT NULL,
    p_ INTEGER,
    d_ INTEGER,
    q_ INTEGER,
    P INTEGER,
    D INTEGER,
    Q INTEGER,
    s INTEGER,
    account_id INTEGER REFERENCES accounts (account_id)
    )
"""

transactionSchema = """
            CREATE TABLE transactions (
                transaction_id serial PRIMARY KEY, 
                account_id INTEGER REFERENCES accounts (account_id), 
                transaction_type TEXT,
                check_number INT,
                payee TEXT,
                transaction_category TEXT,
                total NUMERIC,
                timestamp TIMESTAMP
                )
            """

course_check_id_index = "CREATE INDEX courses_check_fkey ON courses (check_id)"
item_check_id_index = "CREATE INDEX items_check_fkey ON items (check_id)"
item_course_id_index = "CREATE INDEX items_course_fkey ON items (course_id)"

def create_schema():
    commands = (
        "CREATE SCHEMA IF NOT EXISTS dod",

        # "DROP TABLE weather",
        # "DROP TABLE quotes",
        # "DROP TYPE condition_main_enum",
        # f"{condition_main_enum}",
        # f"{weatherSchema}",
        # f"{quotesSchema}",

        # GDP DATA
        # "DROP TABLE food_services_gdp",
        # "DROP TYPE state_enum",
        # f"{state_enum}",
        # f"{food_services_gdp_Schema}"

        #POS DATA
        # "DROP TABLE items",
        # "DROP TABLE courses",
        # "DROP TABLE checks",
        # "DROP TYPE status_enum",
        # "DROP TYPE tax_type_enum",
        # "DROP TYPE day_enum",
        # "DROP TYPE day_of_week_enum",
        # "DROP TYPE month_enum",
        # "DROP TYPE course_type_enum",
        # "DROP TYPE vc_enum",
        # "DROP TYPE vc_reason_enum",
        # "DROP TYPE check_type_enum",
        # f"{status_enum}",
        # f"{tax_type_enum}",
        # f"{day_enum}",
        # f"{day_of_week_enum}",
        # f"{month_enum}",
        # f"{course_type_enum}",
        # f"{vc_enum}",
        # f"{vc_reason_enum}",
        # f"{check_type_enum}",
        # f"{checkSchema}",
        # f"{courseSchema}",
        # f"{itemSchema}",
        # f"{course_check_id_index}",
        # f"{item_check_id_index}",
        # f"{item_course_id_index}",

        # "DROP TABLE IF EXISTS model_parameters",
        # "DROP TABLE IF EXISTS accounts",
        # "DROP TYPE IF EXISTS account_type_enum",
        # "DROP TYPE IF EXISTS model_category_enum",

        # f"{account_type_enum}",
        # f"{model_category_enum}",
        # f"{accounts_Schema}",
        # f"{model_parameters_Schema}",

        # "DROP TABLE IF EXISTS transactionSchema",
        # "DROP TYPE IF EXISTS transaction_type_enum",

        # f"{transaction_type_enum}",
        # f"{transactionSchema}",

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
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


create_schema()