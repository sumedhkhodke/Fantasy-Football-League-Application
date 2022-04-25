import psycopg2
import pandas as pd
import psycopg2.extras as extras
import numpy as np
from config import param_dic

def connect(params_dic):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params_dic)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit(1) 
    return conn

def custom_query(query):
    """
    custom query
    """
    conn = connect(param_dic)
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    cols = [desc[0] for desc in cur.description]
    df = pd.DataFrame(rows, columns=cols)
    cur.close()
    conn.close()
    return df
