
import psycopg2
import pandas as pd
import psycopg2.extras as extras
# from sqlalchemy import create_engine
from io import StringIO
import numpy as np
import os, random
# from psycopg2.extensions import register_adapter, AsIs
# psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)

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
    query  = "INSERT INTO "+table+"("+cols+") VALUES(%s,%s,%s,%s,%s)" 
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

# select unique player ids
conn = connect(param_dic)
cursor = conn.cursor()
postgreSQL_select_Query = "select player_id from player"
cursor.execute(postgreSQL_select_Query)
print("Selecting rows from player table using cursor.fetchall")
player_records = cursor.fetchall()
list_of_player_ids = []
for row in player_records:
    list_of_player_ids.append(row[0])
print(list_of_player_ids)
cursor.close()
conn.close()

# select unique user ids
conn = connect(param_dic)
cursor = conn.cursor()
postgreSQL_select_Query = 'SELECT user_id, username, email, role_type FROM public."user"'
cursor.execute(postgreSQL_select_Query)
print("Selecting rows from user table using cursor.fetchall")
user_records = cursor.fetchall()
user_id_list = []
for row in user_records:
    user_id_list.append(row[0])
print(user_id_list)
cursor.close()
conn.close()

# execute many
conn = connect(param_dic)
cursor = conn.cursor()
user_id_list = random.choices(user_id_list, k=1000)
user_sel_1_list, user_sel_2_list, user_sel_3_list = [], [], []
for i in range(1,1000):
    random_selected = random.sample(list_of_player_ids, 3)
    user_sel_1_list.append(random_selected[0])
    user_sel_2_list.append(random_selected[1])
    user_sel_3_list.append(random_selected[2])

#change this sum of scores
sum_of_scores = [sum(x) for x in zip(user_sel_1_list, user_sel_2_list, user_sel_3_list)]

# add week_id

# finalize dataframe
data = {'user_id':user_id_list,'user_sel_1':user_sel_1_list,'user_sel_2':user_sel_2_list,'user_sel_3':user_sel_3_list,'sum_of_scores':sum_of_scores}
df = pd.DataFrame(data)
df = df.convert_dtypes()
x = execute_many(conn, df, 'user_selection')
conn.close()