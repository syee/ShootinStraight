import goldsberry
import pandas as pd

#set pandas data frame display options
pd.set_option("display.max_columns", 50)
pd.set_option("display.max_rows", 50)

#obtain the game ids
players = goldsberry.PlayerList()
players = pd.DataFrame(players)

print(players)

player_ids = players['PERSON_ID'].tolist()

# print(player_ids)

chart_output = []
print player_ids[0]

for i in range(0,3):
    ex_chart_info = goldsberry.player.shot_chart(player_ids[i])
    chart_output = chart_output + ex_chart_info.chart()

chart_output = pd.DataFrame(chart_output)

# print(chart_output)