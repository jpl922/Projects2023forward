# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 20:37:26 2024
https://www.kaggle.com/code/robikscube/nfl-big-data-bowl-plotting-player-position/notebook
@author: Jason
"""


import numpy as np
import pandas as pd

import os
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as patches



#%% Load Data
Games = pd.read_csv("games.csv")
players = pd.read_csv("players.csv")
plays = pd.read_csv("plays.csv")
W1 = pd.read_csv("week1.csv")


#%% Load weekly Data
openstr = "week"
endstr = ".csv"

weekarray = []
for x in range(17):
    varstr = "W"+str((x+1))
    weekarray.append(varstr)

for y in range(17):
    reindexval = y+1
    midstr = str(reindexval)
    filestr = openstr+midstr+endstr
    weekarray[y] = pd.read_csv(filestr)
   

    



#%% Pull information from the variables 

GamesCol = Games.columns
playerscol = players.columns
playscol = plays.columns
W1Col = W1.columns


    
    
    
