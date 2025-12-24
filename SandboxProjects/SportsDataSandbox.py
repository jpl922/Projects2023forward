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
Michkov = client.edge.skater_detail(player_id='8478387',season='20252026')
MichkovShot = client.edge.skater_shot_location_detail(player_id='8478387',season='20252026')

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


# Shot charts
from nba_api.stats.endpoints import shotchartdetail
# team_id = 0 removes team id requirement 
MaxeyShotData25 = shotchartdetail.ShotChartDetail(team_id=0, player_id=1630178,context_measure_simple='FGA',season_nullable="2025-26",season_type_all_star=['Regular Season']).get_data_frames()[0]
MaxeyShotDataRookie =shotchartdetail.ShotChartDetail(team_id=0, player_id=1630178,context_measure_simple='FGA',season_nullable="2020-21",season_type_all_star=['Regular Season']).get_data_frames()[0]
fig,ax =plt.subplots()
ax.scatter(MaxeyShotDataRookie["LOC_X"].to_numpy(),(MaxeyShotDataRookie["LOC_Y"]).to_numpy())
ax.set_title('Maxey rookie')
fig,ax =plt.subplots()
ax.scatter(MaxeyShotData25["LOC_X"].to_numpy(),(MaxeyShotData25["LOC_Y"]).to_numpy())
ax.set_title('2025-2026')

# why plus 60 for half court?? purely a plotting thing?  
#https://algorithmicathlete.com/blog/is-mid-range-dead

CurryShotData25 = shotchartdetail.ShotChartDetail(team_id=0, player_id=201939,context_measure_simple='FGA',season_nullable="2025-26",season_type_all_star=['Regular Season']).get_data_frames()[0]
CurryShotDataRookie =shotchartdetail.ShotChartDetail(team_id=0, player_id=201939,context_measure_simple='FGA',season_nullable="2009-10",season_type_all_star=['Regular Season']).get_data_frames()[0]
fig,ax =plt.subplots()
ax.scatter(CurryShotDataRookie["LOC_X"].to_numpy(),(CurryShotDataRookie["LOC_Y"]).to_numpy())
ax.set_title('Curry Rookie')
fig,ax =plt.subplots()
ax.scatter(CurryShotData25["LOC_X"].to_numpy(),(CurryShotData25["LOC_Y"]).to_numpy())
ax.set_title('Curry 2025-2026')

VJShotData = shotchartdetail.ShotChartDetail(team_id=0, player_id=1642845,context_measure_simple='FGA',season_nullable="2025-26",season_type_all_star=['Regular Season']).get_data_frames()[0]
fig,ax =plt.subplots()
ax.scatter(VJShotData["LOC_X"].to_numpy(),(VJShotData["LOC_Y"]).to_numpy())
ax.set_title('VJ Rookie')
MccainShotDataRookie = shotchartdetail.ShotChartDetail(team_id=0, player_id=1642272,context_measure_simple='FGA',season_nullable="2024-25",season_type_all_star=['Regular Season']).get_data_frames()[0]
fig,ax =plt.subplots()
ax.scatter(MccainShotDataRookie["LOC_X"].to_numpy(),(MccainShotDataRookie["LOC_Y"]).to_numpy())
ax.set_title('Mccain Rookie')





























