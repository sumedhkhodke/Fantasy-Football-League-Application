
import psycopg2
import pandas as pd
import psycopg2.extras as extras
# from sqlalchemy import create_engine
from io import StringIO
import numpy as np
import os, random
import datetime
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

# select unique teams ids 
conn = connect(param_dic)
cursor = conn.cursor()
postgreSQL_select_Query = 'SELECT team_id, team_name, wins, losses, draws, manager_id, goals_scored, goals_conceded, possession FROM public.team'
cursor.execute(postgreSQL_select_Query)
print("Selecting rows from team table using cursor.fetchall")
team_records = cursor.fetchall()
final_list = []
for row in team_records:
    final_list.append(row[0])
print(final_list)
cursor.close()
conn.close()

final_list = [1,2,3,4,5]
# create fixtures df
f=0
start_date = datetime.date(2021, 8 , 30)
number_of_days = 190
date_list = [(start_date + datetime.timedelta(days = day)).isoformat() for day in range(number_of_days)]
date_list_shuffled = random.sample(date_list, len(date_list))     
df_list = []
print(date_list_shuffled)
date_id=0

#round robin
for i in range(len(final_list)):
    f+=1
    for j in range(i+1,len(final_list)):
        dic={}
        date_id+=1
        dic['fixture_id']=f
        dic['teamid_1']=final_list[i]
        dic['teamid_2']=final_list[j] 
        dic['winning_team_id']=random.choices([final_list[i],final_list[j]], k=1)[0]
        dic['date']=date_list_shuffled[date_id]
        df_list.append(dic)

df = pd.DataFrame(df_list)
print(df)

# execute many
conn = connect(param_dic)
cursor = conn.cursor()
df = df.convert_dtypes()
print("here")
x = execute_many(conn, df, 'fixtures')
conn.close()