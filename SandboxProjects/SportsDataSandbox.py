# -*- coding: utf-8 -*-
"""
Created on Tue Dec 23 16:38:20 2025
Nba and NHL Apis
@author: 17jlo
"""
#%% Import
import numpy as np 
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

#%% NHL
from nhlpy import NHLClient

client =NHLClient()
teams = client.teams.teams()

# Find a specific team
for team in teams:
    if team['abbr'] == 'PHI':
        print(f"Team: {team['name']}")
        print(f"Division: {team['division']['name']}")
        print(f"Franchise ID: {team['franchise_id']}")
        break

# Get that team's roster
roster = client.teams.team_roster(team_abbr="PHI", season="20252026")
print(f"Forwards: {len(roster['forwards'])}")
print(f"Defensemen: {len(roster['defensemen'])}")
print(f"Goalies: {len(roster['goalies'])}")

#Michkov 8484387

#%% NBA
from nba_api.stats.static import players

nba_players = players.get_players()
print("Number of players fetched: {}".format(len(nba_players)))
nba_players[:5]
#VJ 1642845
#Maxey 1630178
#Harden 201935
#Curry 201939
#Mccain 1642272
#embiid 203954

# Career stats
from nba_api.stats.endpoints import playercareerstats

Maxey = playercareerstats.PlayerCareerStats(player_id='1630178')
MaxeyData = Maxey.season_totals_regular_season.get_data_frame()

fig,ax = plt.subplots()

ax.scatter(MaxeyData['SEASON_ID'],MaxeyData['FG3_PCT']*100,s=100*MaxeyData['FG3M']/MaxeyData['GP'], alpha = 0.5)
plt.show()

Curry = playercareerstats.PlayerCareerStats(player_id='201939')
CurryData = Curry.season_totals_regular_season.get_data_frame()
fig, ax = plt.subplots()
ax.scatter(CurryData['SEASON_ID'],CurryData['FG3_PCT']*100,s=100*CurryData['FG3M']/CurryData['GP'], alpha = 0.5)
plt.show()





































