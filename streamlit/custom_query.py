import psycopg2
import pandas as pd
import psycopg2.extras as extras
import numpy as np
import os, sys
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
    try:
        conn = connect(param_dic)
        cur = conn.cursor()
        print(query)
        checks = ['update','insert','delete']
        if any(x in query.lower() for x in checks):
            raise Exception('Not allowed to update, insert or delete')
        cur.execute(query)
        rows = cur.fetchall()
        cols = [desc[0] for desc in cur.description]
        df = pd.DataFrame(rows, columns=cols)
        cur.close()
        conn.close()
        return df
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        cur.close()
        conn.close()
        raise error
        
