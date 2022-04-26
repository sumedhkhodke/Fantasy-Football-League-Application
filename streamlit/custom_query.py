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
        checks = ['update','insert','delete','drop','create','alter','truncate']
        flag1=False
        if any(x in query.lower() for x in checks):
            flag1=True
            df=None
        if not flag1:
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
        
