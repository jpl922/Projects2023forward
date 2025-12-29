# -*- coding: utf-8 -*-
"""
Created on Tue Dec 23 16:38:20 2025
Nba and NHL Apis
@author: 17jlo
"""
#%% General Import
import numpy as np 
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc

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

#%% NBA Imports
from nba_api.stats.static import players
nba_players = players.get_players()
from nba_api.stats.static import teams
nba_teams = teams.get_teams()

#%% NBA Sandbox 
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

#Functions 
# Player ID lookup
# season selector; for loop with len of seasons; 
# data storage; shot chart variable 
# plot generation 
# prereqs
# nba_players
def nba_player_lookup(fullname: str)->dict:
   NBAPID = [player for player in nba_players if player["full_name"]==fullname][0]
   return NBAPID
EmbiidPID = nba_player_lookup("Joel Embiid")['id'] # keep ID only which is all needed


# prereqs
# nba_teams
def nba_team_lookup(teamname: str)-> dict: 
    NBATID = [team for team in nba_teams if team["full_name"] == teamname][0]
    return NBATID
SixerTID = nba_team_lookup("Philadelphia 76ers")['id']
# could shot chart be a class; with function of player lookup, data cleaning, plotting 


# from nba_api.stats.endpoints import playercareerstats
EmbiidCareer = playercareerstats.PlayerCareerStats(EmbiidPID)
EmbiidDataframe = EmbiidCareer.season_totals_regular_season.get_data_frame()
EmbiidSeason = EmbiidDataframe['SEASON_ID'] # index 


from nba_api.stats.endpoints import shotchartdetail

EmbiidSC = {}

for Season in EmbiidSeason:
    data = shotchartdetail.ShotChartDetail(team_id=0, player_id=EmbiidPID,context_measure_simple='FGA',season_nullable=Season,season_type_all_star=['Regular Season']).get_data_frames()[0]
    df = pd.DataFrame(data)
    EmbiidSC[Season]= df

Rookie = EmbiidSC[EmbiidSeason[0]]
fig, ax = plt.subplots()

ax.set_title(EmbiidSeason[0])

# LOC_X and LOC_Y +/- 220 is +/- 22 feet from the center of the hoop 
# therefore, in the axis units 1 foot is 10 units
#https://github.com/bradleyfay/py-Goldsberry/blob/main/docs/Visualizing%20NBA%20Shots%20with%20py-Goldsberry.ipynb
# Draw court

#bradleyfay
# death of mid range

# https://official.nba.com/rule-no-1-court-dimensions-equipment/

#def draw_court(ax = None, color = 'gray', lw = 1, outer_lines=False):
color = 'k'
lw=2
fig,ax = plt.subplots()

made_shots = Rookie[Rookie['SHOT_MADE_FLAG']==1]
missed_shots = Rookie[Rookie['SHOT_MADE_FLAG']==0]
fig,ax = plt.subplots()
ax.scatter(missed_shots["LOC_X"].to_numpy(),(missed_shots["LOC_Y"]+60).to_numpy(),color='r',marker='x',linewidth=1,alpha=0.3)
ax.scatter(made_shots["LOC_X"].to_numpy(),(made_shots["LOC_Y"]+60).to_numpy(),facecolor='none',edgecolor='g',marker='o',linewidth=1,alpha=0.5)
draw_court(ax,lw,color)



# this requires +60 on the shots, 6 ft; shifts data to not be centered with hoop at 0; easier to draw court
def draw_court(ax,lw,color):
    ax.plot([-220,-220],[0,140],linewidth=lw, color=color) # left corner
    ax.plot([220,220],[0,140], linewidth=lw, color=color) # right corner
    ax.add_artist(mpl.patches.Arc((0,140), 440, 315, theta1=0,theta2 = 180, facecolor='none',edgecolor=color,lw=lw)) # 3pt
    ax.plot([-80, -80], [0,190], linewidth=lw,color=color) #outer key left
    ax.plot([80,80], [0,190], linewidth=lw,color=color) #outer key right
    ax.plot([-60,-60], [0,190], linewidth=lw, color=color) # inner lane left
    ax.plot([60,60], [0,190], linewidth=lw, color=color) # inner lane right
    ax.plot([-80,80],[190,190],linewidth=lw,color=color) # top of key
    ax.add_artist(mpl.patches.Circle((0,190), 60, facecolor='none',edgecolor=color, lw =2)) # ft circle
    ax.add_artist(mpl.patches.Circle((0,60), 15, facecolor='none',edgecolor=color, lw =2)) # hoop
    ax.plot([-30,30], [40,40], linewidth=lw, color=color) # back board
    ax.set_xlim(-250,250)
    ax.set_ylim(0,470) # excludes heaves anyways 
    ax.set_xticks([])
    ax.set_yticks([])


# Psuedocode for next steps 
# have the Embiid shoot in a dictionary of DFs
# have way to isolate the seasons
# have way to draw the court 
# have way to select the made and missed shots 
# function made/missed 

# 1. PlayerSeason = usable index of all seasons in career
# 2. PlayerSC = Dictionary of shot data frames 
# 3. Pass PlayerSeason into PlayerSC to isolate data; also made/miss
# 4. plot made/miss for season update legend (want some evolution/event handling)
# 5. draw court

# function made/missed / plot 


# no longer needed code 
# # Collect Player Shot Charts
# PlayerSC = {}
# for Season in PlayerSeason:
#     data = shotchartdetail.ShotChartDetail(team_id=0, player_id=PlayerPID,context_measure_simple='FGA',season_nullable=Season,season_type_all_star=['Regular Season']).get_data_frames()[0]
#     df = pd.DataFrame(data)
#     PlayerSC[Season]= df
# makes={}
# misses={}
# for Season in PlayerSeason: # combine loops and improve efficiency ; broken out here uses
#     df = PlayerSC[Season] # EmbiidSeason[0] is equivalent to Season 
#     madedata=df[df['SHOT_MADE_FLAG']==1]
#     misseddata=df[df['SHOT_MADE_FLAG']==0]
#     makes[Season] = madedata
#     misses[Season] = misseddata

# plotting before figuring out adding subplot and enumerate 
# fig,axs = plt.subplots(2,5,squeeze=False) # issue with the plotting subplots
# #https://stackoverflow.com/questions/66605002/struggling-with-matplotlib-subplots-in-a-for-loop
# idx = 0
# idxrow = 0
# for Season in PlayerSeason:
#     if idx == 5: # needed to fix axes matlab actually way better with indexing 
#         idx = 0
#         idxrow = 1
#     axs[idxrow,idx].plot(misses[Season]["LOC_X"].to_numpy(),(misses[Season]["LOC_Y"]+60).to_numpy(),color='r',marker='x',linewidth=1,alpha=0.3,ls="")
#     axs[idxrow,idx].plot(makes[Season]["LOC_X"].to_numpy(),(makes[Season]["LOC_Y"]+60).to_numpy(),color='g',marker='o',fillstyle = 'none',linewidth=1,alpha=0.5,ls="")
#     draw_court(axs[idxrow,idx],lw,color)
#     #axs[idx].legend(['Missed','Made'])
#     axs[idxrow,idx].set_title(Season)
#     idx += 1
#     print(idx)
#     print("idxrow:"+str(idxrow))
# fig.tight_layout()
# # shot types plotting?


# plotting stucture for function 
# # Plotting need to figure out indexing for subplots and programmatic definition 
# plt.close('all')
# # https://stackoverflow.com/questions/28070906/loop-over-2d-subplot-as-if-its-a-1-d
# fig = plt.figure()
# for idxtest, Season in enumerate(PlayerSeason,start=1): 
#     ax = fig.add_subplot(5,5,idxtest)
#     ax.plot(misses[Season]["LOC_X"].to_numpy(),(misses[Season]["LOC_Y"]+60).to_numpy(),color='r',marker='x',linewidth=1,alpha=0.3,ls="")
#     ax.plot(makes[Season]["LOC_X"].to_numpy(),(makes[Season]["LOC_Y"]+60).to_numpy(),color='g',marker='o',fillstyle = 'none',linewidth=1,alpha=0.5,ls="")
#     draw_court(ax,lw,color)
#     #axs[idx].legend(['Missed','Made'])
#     ax.set_title(Season)
#     fig.tight_layout()
 



#%% Shot Chart clean
# general imports
import numpy as np 
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc
#%matplotlib qt # run current line to get around syntax error 

# API imports
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.static import players # needed for player lookup
nba_players = players.get_players() # needed for player lookup
from nba_api.stats.static import teams # needed for team lookup
nba_teams = teams.get_teams() # needed for team lookup 





# Plot Settings
color = 'w' # court line color
lw=2 # court linewidth
ncol = 4
plt.style.use('dark_background')

# Variables
PlayerName = "James Harden"

# Shot Chart Lookup Settings 
# reserved for future use

# Functions 
def nba_team_lookup(teamname: str)-> dict: 
 # Returns dictionary containing the Player ID of a player 
    NBATID = [team for team in nba_teams if team["full_name"] == teamname][0]
    return NBATID
def nba_player_lookup(fullname: str)->dict:
    # Returns dictionary containingt he Team ID of a team 
   NBAPID = [player for player in nba_players if player["full_name"]==fullname][0]
   return NBAPID
def draw_court(ax,lw,color):
    # draws court based on the NBA LOC shot chart details 
    ax.plot([-220,-220],[0,140],linewidth=lw, color=color) # left corner
    ax.plot([220,220],[0,140], linewidth=lw, color=color) # right corner
    ax.add_artist(mpl.patches.Arc((0,140), 440, 315, theta1=0,theta2 = 180, facecolor='none',edgecolor=color,lw=lw)) # 3pt
    ax.plot([-80, -80], [0,190], linewidth=lw,color=color) #outer key left
    ax.plot([80,80], [0,190], linewidth=lw,color=color) #outer key right
    ax.plot([-60,-60], [0,190], linewidth=lw, color=color) # inner lane left
    ax.plot([60,60], [0,190], linewidth=lw, color=color) # inner lane right
    ax.plot([-80,80],[190,190],linewidth=lw,color=color) # top of key
    ax.add_artist(mpl.patches.Circle((0,190), 60, facecolor='none',edgecolor=color, lw =2)) # ft circle
    ax.add_artist(mpl.patches.Circle((0,60), 15, facecolor='none',edgecolor=color, lw =2)) # hoop
    ax.plot([-30,30], [40,40], linewidth=lw, color=color) # back board
    ax.set_xlim(-250,250)
    ax.set_ylim(0,470) # excludes heaves anyways 
    ax.set_xticks([])
    ax.set_yticks([])
def get_player_shotchart(SeasonsPlayed)->dict:
    # input is list of nba seasons for player PlayerSeason; output dataframes and make/miss
    #pre-allocation
    PlayerSC={}
    makes={}
    misses={}
    # for loop 
    for Season in SeasonsPlayed:
        data = shotchartdetail.ShotChartDetail(team_id=0, player_id=PlayerPID,context_measure_simple='FGA',season_nullable=Season,season_type_all_star=['Regular Season']).get_data_frames()[0]
        df = pd.DataFrame(data)
        PlayerSC[Season]=df
        makes[Season] = df[df['SHOT_MADE_FLAG']==1]
        misses[Season] = df[df['SHOT_MADE_FLAG']==0]
    return(PlayerSC, makes, misses)

def Plot_player_shotchart(PlayerName:str,SeasonsPlayed,ncol:int):
    plt.close('all')
    fig = plt.figure()
    fig.suptitle(PlayerName)
    fig.tight_layout()
    PlayerSeason = SeasonsPlayed
    
    quotient, remainder = divmod(len(PlayerSeason),ncol)
    nrow =  quotient
    if remainder:
        nrow = quotient + 1
    
    for idxtest, Season in enumerate(PlayerSeason,start=1): 
        ax = fig.add_subplot(nrow,ncol,idxtest)
        ax.plot(misses[Season]["LOC_X"].to_numpy(),(misses[Season]["LOC_Y"]+60).to_numpy(),color='r',marker='x',linewidth=1,alpha=0.6,ls="")
        ax.plot(makes[Season]["LOC_X"].to_numpy(),(makes[Season]["LOC_Y"]+60).to_numpy(),color='g',marker='o',fillstyle = 'none',linewidth=1,alpha=0.6,ls="")
        draw_court(ax,lw,color)
        ax.set_title(Season)
    # Shot Plot Note +60 is a coordinate correction for the half court / coordinates


# ID Lookup 
PlayerPID = nba_player_lookup(PlayerName)['id'] # keep ID only which is all needed
SixerTID = nba_team_lookup("Philadelphia 76ers")['id']

# Determine Player Seasons (Index)
PlayerCareer = playercareerstats.PlayerCareerStats(PlayerPID)
PlayerDataframe = PlayerCareer.season_totals_regular_season.get_data_frame()
PlayerSeason = PlayerDataframe['SEASON_ID'] # index 

# Function Calls 
PlayerSC, makes, misses = get_player_shotchart(PlayerSeason)
Plot_player_shotchart(PlayerName,PlayerSeason,ncol)

#%% figuring out subplot indexing

# # https://stackoverflow.com/questions/24828771/automate-the-populating-of-subplots

# col = 4 
# nseason = 2
# quotient, remainder = divmod(nseason,col)
# rows = quotient
# print(rows)
# if remainder: 
#     rows = rows+1
# print("new:"+str(rows))
  









