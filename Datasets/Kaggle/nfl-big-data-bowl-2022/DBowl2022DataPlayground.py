# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 20:04:27 2024

@author: Jason
"""

import os
import numpy as np
import pandas as pd
import matplotlib as mpl



#%% Load Data
Games = pd.read_csv("games.csv")
Scout = pd.read_csv("PFFScoutingData.csv")
players = pd.read_csv("players.csv")
plays = pd.read_csv("plays.csv")
Tracking2018 = pd.read_csv("tracking2018.csv")
Tracking2019 = pd.read_csv("tracking2019.csv")
Tracking2020 = pd.read_csv("tracking2020.csv")

#%% Pull information from the variables 

GameCol = Games.columns
ScoutCol = Scout.columns
playerscol = players.columns
playscol = plays.columns
Tracking2018col = Tracking2018.columns
Tracking2019col = Tracking2019.columns
Tracking2020 = Tracking2020.columns
