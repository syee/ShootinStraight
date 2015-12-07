import matplotlib
import requests
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.patches import Circle, Rectangle, Arc

def generate_shot_chart_url(player, startYear, endYear):
	shot_chart_url = 'http://stats.nba.com/stats/shotchartdetail?CFID=33&CFPAR'\
	'AMS=' + str(startYear) + '-' + str((endYear%100)) + '&ContextFilter=&ContextMeasure=FGA&DateFrom=&D'\
	'ateTo=&GameID=&GameSegment=&LastNGames=0&LeagueID=00&Loca'\
	'tion=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&'\
	'PaceAdjust=N&PerMode=PerGame&Period=0&PlayerID='+ str(player)+ '&Plu'\
	'sMinus=N&Position=&Rank=N&RookieYear=&Season=' + str(startYear) + '-' + str((endYear%100)) + '&Seas'\
	'onSegment=&SeasonType=Regular+Season&TeamID=0&VsConferenc'\
	'e=&VsDivision=&mode=Advanced&showDetails=0&showShots=1&sh'\
	'owZones=0'
	return shot_chart_url

def draw_court(ax=None, color='black', lw=2, outer_lines=False):
	if ax is None:
		ax = plt.gca()

	hoop = Circle((0,0), radius=7.5, linewidth=lw, color=color, fill=False)
	backboard = Rectangle((-30,-7.5), 60, -1, linewidth=lw, color=color)
	outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color, fill=False)
	inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color, fill=False)
	top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180, linewidth=lw, color=color, fill=False)
	bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color, linestyle='dashed')
	restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw, color=color)
	corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw, color=color)
	corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
	three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw, color=color)
	center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color)
	center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0, linewidth=lw, color=color)
	court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                      bottom_free_throw, restricted, corner_three_a,
                      corner_three_b, three_arc, center_outer_arc,
                      center_inner_arc]

	if outer_lines:
		outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw, color=color, fill=False)
		court_elements.append(outer_lines)


	for element in court_elements:
		ax.add_patch(element)

	return ax

def generate_shot_chart(playerID, playerName, startYear, endYear):
	shot_chart_url = generate_shot_chart_url(playerID, startYear, endYear)
	response = requests.get(shot_chart_url)
	headers = response.json()['resultSets'][0]['headers']
	shots = response.json()['resultSets'][0]['rowSet']
	shot_df = pd.DataFrame(shots, columns=headers)

	sns.set_style("white")
	sns.set_color_codes()

	joint_shot_chart = sns.jointplot(shot_df.LOC_X, shot_df.LOC_Y, stat_func=None, kind='scatter', space=0, alpha=0.5)
	joint_shot_chart.fig.set_size_inches(12,11)

	# A joint plot has 3 Axes, the first one called ax_joint 
	# is the one we want to draw our court onto and adjust some other settings
	ax = joint_shot_chart.ax_joint
	draw_court(ax)

	# Adjust the axis limits and orientation of the plot in order
	# to plot half court, with the hoop by the top of the plot
	ax.set_xlim(-250,250)
	ax.set_ylim(422.5, -47.5)

	# Get rid of axis labels and tick marks
	ax.set_xlabel('')
	ax.set_ylabel('')
	ax.tick_params(labelbottom='off', labelleft='off')

	# Add a title
	ax.set_title('\n' + playerName + ' FGA ' + ' 2014-15 Reg. Season', 
	             y=1.2, fontsize=18)

	# Add Data Scource and Author
	ax.text(-250,445,'Data Source: stats.nba.com'
	        '\nAuthor: Savvas Tjortjoglou (savvastjortjoglou.com)',
	        fontsize=12)

	plt.show()










