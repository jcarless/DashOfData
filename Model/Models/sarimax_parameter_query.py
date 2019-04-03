#get_params(
#   model_category: model_category_enum - What model is being run ex: sarimax, 
#    seasons: Numeric - s value aka number of seasonal periods,
#   account_id: Integer - id of the account the model is being run for)

def get_params(model_category, seasons, account_id):
    import psycopg2
    import pandas as pd
    import os, sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from db_functions import db_connection, db_close
    
    conn, cur = db_connection()
    sql = f"""
           SELECT "p_", "d_", "q_", "p", "d", "q", "s", "parameter_id" FROM "public"."model_parameters" 
            WHERE "model_category" = '{model_category}'
            AND "s" = {seasons}
            AND "account_id" = {account_id}
            ORDER BY "date" DESC
            LIMIT 1
           """
          
    try:           
       cur.execute(sql)
       parameters = cur.fetchall()
       parameters = pd.DataFrame(parameters, columns=["p", "d", "q", "P", "D", "Q", "s", "parameter_id"])
       p = parameters["p"][0]
       d = parameters["d"][0]
       q = parameters["q"][0]
       P = parameters["P"][0]
       D = parameters["D"][0]
       Q = parameters["Q"][0]
       s = int(parameters["s"][0])
       parameter_id = int(parameters["parameter_id"][0])
       
       return p,d,q,P,D,Q,s,parameter_id

    except (Exception, psycopg2.DatabaseError) as error:
       raise error
    finally:
        db_close(conn, cur)