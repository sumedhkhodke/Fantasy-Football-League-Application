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

def custom_query(query,username):
    """
    custom query
    """
    try:
        conn = connect(param_dic)
        cur = conn.cursor()
        checks = ['update','insert','delete','drop','create','alter','truncate']
        flag1=False
        usernames_list = get_admin_list()
        if any(x in query.lower() for x in checks) and(username not in usernames_list):
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

def get_admin_list():
    conn = connect(param_dic)
    cursor = conn.cursor()
    postgreSQL_select_Query = 'SELECT username FROM public."user" where role_type=\'admin\';'
    cursor.execute(postgreSQL_select_Query)
    username_records = cursor.fetchall()
    usernames_list = []
    for row in username_records:
        usernames_list.append(row[0])
    cursor.close()
    conn.close()
    return usernames_list
        
