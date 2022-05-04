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
    logo_image = Image.open('dmql_logo.jpeg')
    st.sidebar.image(logo_image, use_column_width=True)
    navigate = st.sidebar.radio('Menu',['About the application','List of Tables','ER diagram','List of Queries','Run Select Query','Run Custom Query','About Us'])

    if navigate == 'About the application':
        st.markdown("""
        # Fantasy Football League
        Fantasy Football League is an application where users select the players of their choice from the available list. These players are scored every week based on their real time performances with respect to the number of goals scored, assists and many other parameters. The sum of the scores of players selected by the user is the score for the user. At the end of the competition, the winner is decided based on the total score of the user.
        ## Features:
        - There can be two types of Users: 
            - Participant
            - Admin
        - Participant can select player of his choice based on the available statistics and Admin is responsible for managing and updating the database.
        - Following is the points scoring rubric:
            - goal scored : + 5 points
            - assist : +3 points
            - game played : +1 point 
            - foul committed : -1 point

        ## Target User:
        Football fanatics who love the game and want to manage their own teams based on their choice of players.
        """)
    if navigate == 'List of Tables':
        st.markdown("""
        # Tables in the Database
        - User
        - Player
        - Team
        - Manager
        - Fixtures
        - Player_Stats
        - User_Selection
        - User_Leaderboard
        """)
    if navigate == "ER diagram":
        st.markdown("""
        # ER diagram
        """)
        ER_diag = Image.open('NEW_ER.jpeg')
        st.image(ER_diag,width = 750)
    
    if navigate == 'List of Queries':
        st.markdown("""
        # List of Queries
        - SELECT QUERY
            - To get the goals scored by each team :
            select t.team_name,sum(p.assist) assi,sum(p.goals_scored) gsc,sum(p.num_fouls) nf 
            from player p, team t 
            where p.team_id=t.team_id 
            group by t.team_name order by gsc desc;
            
            - To get the number of times a player is selected in fantasy team :
            select player_id,p.player_name,count(p.player_id) cp 
            from player p,user_selection usel 
            where p.player_id=user_sel_1 
            group by p.player_id,p.player_name ;

            - To get the player with maximum fantasy score :
            select player_id,p.player_name,count(p.player_id) cp 
            from player p,user_selection usel 
            where p.player_id=user_sel_1 
            group by p.player_id,p.player_name ;

            - To get the team with least number of fouls
            select p.team_id,t.team_name,sum(num_fouls) as foul 
            from player p, team t 
            where p.team_id=t.team_id 
            group by p.team_id,t.team_name order by foul LIMIT 1;

            - To get the number of managers representing each country
            SELECT count(manager_id),m.country
            from manager m 
            group by m.country;

            - To get the number of players representing each country
            SELECT count(player_id),p.country from player p group by p.country;

            - To get list of players
                - With Inner Join
                select player_id,player_name,t.team_name 
                from player p
                inner join team t 
                on p.team_id=t.team_id;

                - With cartesian product
                select player_id,player_name,t.team_name 
                from player p,team t 
                where p.team_id=t.team_id;

        - UPDATE QUERY
            - To update the playerscore based on goals, assists and fouls by a player
            UPDATE player_stats ps 
            SET ps.fscore = p.games_played + (5 * p.goals_scored) + (3 * p.assist) - p.num_fouls

            - To update the leaderboard based on the total fantasy score of the user
            UPDATE user_leaderboard ul 
            SET ul.sum_of_scores = us.sum_of_scores 
            FROM user_selection us 
            WHERE us.user_id=ul.user_id GROUP BY us.user_id;

        - INSERT QUERY
            - To insert a new player in the player table
            INSERT INTO player 
            VALUES(301, 'Bhaichung Bhutia', 'ATT', 12, 5, 15, 1, 86, 'India', 6, 37)
            - To insert a new user in the user table
            INSERT INTO user VALUES(1010, 'shyam', 'shyam@abc.edu', 'user')

        - DELETE QUERY
            - DELETE FROM player WHERE player_id = '<insert player id>' CASCADE
            - DELETE FROM "user" WHERE user_id = '<insert user id>' CASCADE

        - TRIGGER
            - Trigger to update multiple tables when a related table is updated : 
                - CREATE TRIGGER update_fscore ON player p
                AFTER UPDATE
                AS
                BEGIN
                UPDATE player_stats ps SET 
                ps.fscore = p.games_played + (5 * p.goals_scored) + (3 * p.assist) - p.num_fouls
                END

                - CREATE TRIGGER update_leaderboard ON user_selection us
                AFTER INSERT OR UPDATE
                AS
                BEGIN
                UPDATE user_leaderboard ul 
                SET ul.sum_of_scores = us.sum_of_scores 
                FROM user_selection us 
                WHERE us.user_id=ul.user_id GROUP BY us.user_id;
                END
        """)

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

    if navigate == "About Us":
        st.markdown("""
        # About Us
        """)
        st.markdown("""
        ## Team Name:
        Hackstreet Boys
        ## Team Members:
        - Omkar Rajguru (orajguru@buffalo.edu) - 50414754
        - Saiteja Mattam (saitejam@buffalo.edu) - 50412146
        - Sumedh Khodke (sumedhk@buffalo.edu) - 50419157
        """)
except Exception as e:
    print(e)
    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
    st.error("Looks like something is not right!")
    st.error("Please contact site admin")
