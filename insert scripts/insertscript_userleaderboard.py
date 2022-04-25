
import psycopg2
import pandas as pd
import psycopg2.extras as extras
# from sqlalchemy import create_engine
from io import StringIO
import numpy as np
import os, random
# from psycopg2.extensions import register_adapter, AsIs
# psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)

import numpy
from psycopg2.extensions import register_adapter, AsIs
def addapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)
def addapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)
register_adapter(numpy.float64, addapt_numpy_float64)
register_adapter(numpy.int64, addapt_numpy_int64)

param_dic = {
    "host"      : "localhost",
    "database"  : "test1",
    "user"      : "postgres",
    "password"  : "neww"
}

def connect(params_dic):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params_dic)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit(1) 
    print("Connection successful")
    return conn

def execute_many(conn, df, table):
    """
    Using cursor.executemany() to insert the dataframe
    """
    # Create a list of tupples from the dataframe values
    tuples = [tuple(x) for x in df.to_numpy()]
    # Comma-separated dataframe columns
    cols = ','.join(list(df.columns))
    # SQL quert to execute
    print(cols)
    print(table)
    query  = "INSERT INTO "+table+"("+cols+") VALUES(%s,%s,%s)" 
    # query  = "INSERT INTO %s(%s) VALUES(%%s,%%s,%%s)" % (table, cols)
    cursor = conn.cursor()
    try:
        cursor.executemany(query, tuples)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    print("execute_many() done")
    cursor.close()

# select unique userselection ids and create userleaderboard df
conn = connect(param_dic)
cursor = conn.cursor()
postgreSQL_select_Query = 'SELECT user_id, user_sel_1, user_sel_2, user_sel_3, sum_of_scores FROM public.user_selection'
cursor.execute(postgreSQL_select_Query)
print("Selecting rows from userselection table using cursor.fetchall")
user_sel_records = cursor.fetchall()
final_list = []
for row in user_sel_records:
    dic={}
    dic['user_id'] = row[0]
    dic['sum_of_scores'] = row[4]
    final_list.append(dic)
# print(user_sel_records)
cursor.close()
conn.close()

#preprocess df
df = pd.DataFrame(final_list)
# print(final_list)
df1 = df.groupby('user_id',as_index=False).sum()
df1.sort_values(by=['sum_of_scores'], ascending=False, inplace=True)
df1['rank_id'] = np.arange(1, len(df1)+1)
df1.reset_index(drop=True)

# execute many
conn = connect(param_dic)
cursor = conn.cursor()
df = df.convert_dtypes()
print("here")
x = execute_many(conn, df1, 'user_leaderboard')
conn.close()