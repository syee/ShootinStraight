import goldsberry
import pandas as pd
import requests
import savorgas2
import psycopg2
from sqlalchemy import create_engine


#set pandas data frame display options
pd.set_option("display.max_columns", 50)
pd.set_option("display.max_rows", 50)

#obtain the game ids
def init_players(year):
	players_2014 = goldsberry.PlayerList()
	players_2014 = pd.DataFrame(players_2014)
	# print players
	# engine = create_engine('postgresql:///ShootinStraight')
	# newTable = "players_" + str(year)
	# players.to_sql(newTable, engine)
	return players_2014

def init_games():
	gameids = goldsberry.GameIDs()
	gameids = pd.DataFrame(gameids)

	# engine = create_engine('postgresql:///ShootinStraight')
	# newTable = "games"
	# gameids.to_sql(newTable, engine)
	return gameids

def generate_shotChart(player):
	year1 = 2014
	year2 = year1 + 1
	# print players.ix[0]
	if (not (players.ix[players['PERSON_ID'] == player].empty)):
		print "Hello"
		print players.ix[players['PERSON_ID'] == player]
		print
		print players.ix[players['PERSON_ID'] == player].values.tolist()
		print
		print players.ix[players['PERSON_ID'] == player].values[0]
		print 
		# prints player's name DISPLAY_LAST_COMMA_FIRST
		playerName =  players.ix[players['PERSON_ID'] == player].values.tolist()[0][0]
		print playerName
		playerID =  players.ix[players['PERSON_ID'] == player].iloc[0][3]
		# savorgas2.generate_shot_chart(playerID, playerName, year1, year2)
		# print players.ix[players['PERSON_ID'] == player]['DISPLAY_LAST_COMMA_FIRST'] + " ME"

def generate_shot_chart2(playerID, playerName, year1, year2):
	# year1 = 2014
	# year2 = year1 + 1
	# print players.ix[0]
	# prints player's name DISPLAY_LAST_COMMA_FIRST
	# playerName =  players.ix[players['PERSON_ID'] == player].iloc[0][0]
	# playerID =  players.ix[players['PERSON_ID'] == player].iloc[0][3]
	savorgas2.generate_shot_chart(playerID, playerName, year1, year2)
	savorgas2.generate_shot_chart_makes_misses(playerID, playerName, year1, year2)
	# print players.ix[players['PERSON_ID'] == player]['DISPLAY_LAST_COMMA_FIRST'] + " ME"



# players = init_players(2014)
# players.to_csv("shots.csv")
DB = psycopg2.connect("dbname=ShootinStraight")
c = DB.cursor()
query = "SELECT * from players_2014 where \"DISPLAY_LAST_COMMA_FIRST\"='Bryant, Kobe'"
c.execute(query)
for row in c.fetchall():
	# print row
	print row[4]
	print row[1]
	generate_shot_chart2(int(row[4]), str(row[1]), 2015, 2016)
	# generate_shot_chart2(201935, 'Harden, James', 2014, 2015)


# variableName = 'Korver, Kyle'
# playerIDS = players.ix[players['DISPLAY_LAST_COMMA_FIRST'] == variableName].values[0][3]
# print playerIDS
# print variableName
# generate_shot_chart2(playerIDS, variableName, 2014, 2015)

# init_games()