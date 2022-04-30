import streamlit as st 
import pandas as pd
import numpy as np
import select_query, custom_query
from PIL import Image
import os, sys
import streamlit as st
import streamlit_authenticator as stauth

names = ['Sumedh','Omkar','Saiteja','ron']
usernames = ['sumedh','omkar','saiteja','ron']
passwords = ['dmql@123','dmql@123','dmql@123','dmql@123']

hashed_passwords = stauth.Hasher(passwords).generate()

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
   'some_cookie_name', 'some_signature_key', cookie_expiry_days=0)

try:
    navigate = st.sidebar.radio('Menu',['About The Application','ER diagram','Run Select Query','Run Custom Query'])

    if navigate == 'About The Application':
        st.markdown("""
        # Fantasy Football League
        This application is designed to help you manage your fantasy football league and monitor the leaderboard.
        """)

    if navigate == "ER diagram":
        st.markdown("""
        # ER diagram
        """)
        ER_diag = Image.open('New_ER.png')
        st.image(ER_diag,width = 750)

    if navigate == "Run Select Query":
        table_name = st.selectbox("Select a table to run the SELECT query on:",['User','User_leaderboard','User_selection','Player','Player_stats','Team','Manager','Fixtures'])
        df = select_query.select_query(table_name)
        st.write("")
        st.dataframe(df,width = 15000,height = 500)

    if navigate == "Run Custom Query":
        name, authentication_status, username = authenticator.login('Login', 'sidebar')
        if authentication_status:
            st.write("You are executing database queries as *%s*" % (name))
            c_query = st.text_input('Enter your custom query :','SELECT * FROM public.player;')
            df = custom_query.custom_query(c_query,username)
            if df is None:
                st.write("You do not have enough permissions to run this query")
            else:
                st.write("")
                st.dataframe(df,width = 15000,height = 500)
            if st.session_state['authentication_status']:
                authenticator.logout('Logout', 'sidebar')
        elif authentication_status == False:
            st.error("Username/password is incorrect")
        elif authentication_status == None:
            st.warning("Please enter your username and password")

except Exception as e:
    print(e)
    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
    st.error("Looks like something is not right!")
    st.error("Please contact site admin")
