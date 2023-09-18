# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 17:35:23 2023
Specific file to work on data manipulations without extra code
clearer documentation
@author: 17jlo
"""


# Imports 
import fastf1 as ff1
import fastf1.plotting
import matplotlib as mpl
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
import pandas as pd


#%% Schedule, qualifying, etc... Fastest Lap
schedule = fastf1.get_event_schedule(2023)


# Driver results need this session for scoring
session = fastf1.get_session(2023,'Silverstone','Q')
session.load()
results = session.results # qualifying results 2023 silverstone


top10q = session.results.iloc[0:10].loc[:, ['Abbreviation','Q3']]
top10q = session.results.iloc[0:10].loc[:, ['Abbreviation','Q2']]


# Laps and times 

fastest_lap = session.laps.pick_fastest()
flap = fastest_lap['LapTime']
fdrive = fastest_lap['Driver']


#%% Datamanips


session = fastf1.get_session(2023,'Silverstone','R') # Q will give all quali.
session.load(telemetry=False, weather=False)
raceresults = session.results # watch this give everything HAHAHA just not lap times




# 3 letter abbreviation for each driver gives lap content 
drvdict = {}
for drv in session.drivers: # can do for loops through the list nice 
    drv_laps = session.laps.pick_driver(drv) # saves all stats each driver
    
    # saves all the data into dictionary 
    drvdict[drv] = pd.DataFrame(data = drv_laps)  

# dictionary to list
drvlist1 = [df for df in drvdict.values()]
# combine the dataframes into a single frame 
drvcombine1 = pd.concat(drvlist1,ignore_index=True)


# Laps and times 
fastest_lap = session.laps.pick_fastest()
flap = fastest_lap['LapTime']
fdrive = fastest_lap['Driver']


# scoring thoughts (overtakes not worth it)
# but score positions gain/loss, FLap, Fs1,Fs2,Fs3
# longest tire ware each compound






# Laps and times 
