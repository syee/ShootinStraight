import goldsberry
import pandas as pd
import requests

#set pandas data frame display options
pd.set_option("display.max_columns", 50)
pd.set_option("display.max_rows", 50)

#obtain the game ids
players = goldsberry.PlayerList()
players = pd.DataFrame(players)

# print(players)

player_ids = players['PERSON_ID'].tolist()

# print(player_ids)

#chart_output = []

#for i in player_ids:
#    ex_chart_info = goldsberry.player.shot_chart(i)
#    chart_output =  ex_chart_info.chart()
#    chart_output = pd.DataFrame(chart_output)
#    print(chart_output)

#chart_output = pd.DataFrame(chart_output)

#print(chart_output)

# for i in player_ids:
#     player_string = "PlayerID=" + str(i)

#     shot_chart_url = 'http://stats.nba.com/stats/shotchartdetail?CFID=33&CFPARAMS=2014-15&ContextFilter=&ContextMeasure=FGA&DateFrom=&DateTo=&GameID=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PaceAdjust=N&PerMode=PerGame&Period=0&' + player_string +'&PlusMinus=N&Position=&Rank=N&RookieYear=&Season=2014-15&SeasonSegment=&SeasonType=Regular+Season&TeamID=0&VsConference=&VsDivision=&mode=Advanced&showDetails=0&showShots=1&showZones=0'

#     # Get the webpage containing the data
#     response = requests.get(shot_chart_url)
#     # Grab the headers to be used as column headers for our DataFrame
#     headers = response.json()['resultSets'][0]['headers']
#     # Grab the shot chart data
#     shots = response.json()['resultSets'][0]['rowSet']

#     shot_df = pd.DataFrame(shots, columns=headers)
#     shot_df.to_csv("shots" + player_string + ".csv")

for i in range(0,1):
    player_string = "PlayerID=" + str(player_ids[i])

    shot_chart_url = 'http://stats.nba.com/stats/shotchartdetail?CFID=33&CFPARAMS=2014-15&ContextFilter=&ContextMeasure=FGA&DateFrom=&DateTo=&GameID=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PaceAdjust=N&PerMode=PerGame&Period=0&' + player_string +'&PlusMinus=N&Position=&Rank=N&RookieYear=&Season=2014-15&SeasonSegment=&SeasonType=Regular+Season&TeamID=0&VsConference=&VsDivision=&mode=Advanced&showDetails=0&showShots=1&showZones=0'

    # Get the webpage containing the data
    response = requests.get(shot_chart_url)
    # Grab the headers to be used as column headers for our DataFrame
    headers = response.json()['resultSets'][0]['headers']
    # Grab the shot chart data
    shots = response.json()['resultSets'][0]['rowSet']

    shot_df = pd.DataFrame(shots, columns=headers)
    shot_df.head().to_csv("shots" + player_string + ".csv")
    # View the head of the DataFrame and all its columns
    from IPython.display import display
    with pd.option_context('display.max_columns', None):
       display(shot_df.head())