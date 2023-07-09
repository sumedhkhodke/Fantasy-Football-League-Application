# Fantasy Football League Application

Since the introduction of the internet, the sports betting industry, particularly fantasy football, has grown to be a multi-billion-dollar industry. All aspects of fantasy sports, such as the amount of money, the number of hours, and the number of leagues, are rapidly increasing. The purpose of building a fantasy football league application is to provide an interface to the user to create and manage a team of his/her choice and compete with other users. The main aim of our project is to design a database that hosts a competition between users who follow the game of football. Fantasy Football League is an application where users select the players of their choice. These players are scored every week based on their real time performances with respect to the number of goals scored, assists, and many other parameters. The sum of the scores of players selected by the user is the user's score. At the end of the competition, the winner is decided based on the total score of the user.

Keywords—user, player, fantasy score, fixtures, leaderboard, selection

## Steps to reproduce
In pgadmin, create an empty database

### Steps to Create Tables
1) Open the file "Create Scripts.txt"
2) Run each block of create query in pgadmin in the following order of tables
	- Manager table
	- Team table
	- Player table
	- Player stats table
	- Fixtures table
	- User table
	- User selection table
	- User leaderboard table

### Steps to Insert data in the tables
1) Open cmd and install python 3.x
2) Install psycopg2 package for postgres database connection using python
'''pip install psycopg2'''
3) Run the following commands in order to insert values into respective tables
	- python insertscript_manager.py
	- python insertscript_team.py
	- python insertscript_player.py
	- python insertscript_playerstats.py
	- python insertscript_fixtures.py
	- python insertscript_userselection.py
	- python insertscript_userleaderboard.py
	
Once all queries have executed successfully, the database is ready to use with all inserted values.
