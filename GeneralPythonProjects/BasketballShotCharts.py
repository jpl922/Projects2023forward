# -*- coding: utf-8 -*-
"""
Created on Thu Jan  1 12:45:27 2026
Python File using NBA API to plot Player Shot Charts over their career
Collects shot data and updates the subplots automatically 

Notes Tracked in Obisidian
Derived from SportsDataSandbox into standalone file 
@author: Jason Lord
"""

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
PlayerName = "Joel Embiid"

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