import psycopg2

def db_connection():
    #Create a connection to RDS
    try:
        from config import config 

        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        
        return conn, cur
    
    except (Exception, psycopg2.DatabaseError) as error:
        raise error
        
def db_close(conn=None):
    #End the session
    if conn is not None:
        conn.close()