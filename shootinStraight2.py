import goldsberry
import pandas as pd
import requests
import savorgas2

#set pandas data frame display options
pd.set_option("display.max_columns", 50)
pd.set_option("display.max_rows", 50)

#obtain the game ids
def init_players(year):
	players = goldsberry.PlayerList(AllTime=True)
	players = pd.DataFrame(players)

	# engine = create_engine('postgresql:///ShootinStraight')
	# newTable = "Players_" + year
	# df.to_sql(newTable, engine)
	return players

def init_games():
	gameids = goldsberry.GameIDs()
	gameids = pd.DataFrame(gameids)

	engine = create_engine('postgresql:///ShootinStraight')
	newTable = "Games"
	df.to_sql(newTable, engine)
	return gameids

def generate_shotChart(player):
	year1 = 2014
	year2 = year1 + 1
	# print players.ix[0]
	if (not (players.ix[players['PERSON_ID'] == player].empty)):
		print "Hello"
		# prints player's name DISPLAY_LAST_COMMA_FIRST
		playerName =  players.ix[players['PERSON_ID'] == player].iloc[0][0]
		playerID =  players.ix[players['PERSON_ID'] == player].iloc[0][3]
		savorgas2.generate_shot_chart(playerID, playerName, year1, year2)
		# print players.ix[players['PERSON_ID'] == player]['DISPLAY_LAST_COMMA_FIRST'] + " ME"

def generate_shotChart2(player):
	year1 = 2014
	year2 = year1 + 1
	# print players.ix[0]
	# prints player's name DISPLAY_LAST_COMMA_FIRST
	# playerName =  players.ix[players['PERSON_ID'] == player].iloc[0][0]
	# playerID =  players.ix[players['PERSON_ID'] == player].iloc[0][3]
	savorgas2.generate_shot_chart(201935, "Harden, James", year1, year2)
	# print players.ix[players['PERSON_ID'] == player]['DISPLAY_LAST_COMMA_FIRST'] + " ME"



players = init_players(2014)
# players.to_csv("shots.csv")
# print players.ix[players['DISPLAY_LAST_COMMA_FIRST'] == 'Exum, Dante']
generate_shotChart(201935)

# init_games()