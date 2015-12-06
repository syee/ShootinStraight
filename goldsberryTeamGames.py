import goldsberry
import pandas as pd

pd.set_option("display.max_columns", 50)
print goldsberry.__version__

gameids = goldsberry.GameIDs()
gameids = pd.DataFrame(gameids)

filter_season = '2006'
teamids_2006 = gameids['HOME_TEAM_ID'].ix[gameids['SEASON'] == filter_season].drop_duplicates().tolist()

def get_team_info(teamids):
	teamids_full = []
	for i in teamids:
		team = goldsberry.team.team_info(i)
		teamids_full = teamids_full + team.info()
	return teamids_full

# teams_2006 = get_team_info(teamids_2006)
# teams_2006 = pd.DataFrame(teams_2006)

# print teams_2006.ix[teams_2006['TEAM_NAME'].str.contains('Lakers')]

suns_id = 1610612756
suns_logs = goldsberry.team.game_logs(suns_id, season = '2006')
suns_logs = pd.DataFrame(suns_logs.logs())

suns_2006_dec_jan = suns_logs['Game_ID'].ix[suns_logs['GAME_DATE'].str.contains('JAN|DEC')].tolist()

def get_box_score_player_info(gameids):
	bs_info = []
	for i in gameids:
		info = goldsberry.game.boxscore_traditional(i, rangetype = 0)
		bs_info = bs_info + info.player_stats()
	return bs_info

player_box_info = get_box_score_player_info(suns_2006_dec_jan)
player_box_info = pd.DataFrame(player_box_info)

print player_box_info.ix[player_box_info['PLAYER_NAME'] == "Steve Nash"]




# playersCurrent = pd.DataFrame(goldsberry.PlayerList(2014))
# playersCurrent.head()