# -*- coding: utf-8 -*-
"""
Messing around with FastF1 (plotting, data, and events)
Figure out how to code overtakes

@author: JL_22
"""

# Imports 
import fastf1 as ff1
import fastf1.plotting
import matplotlib as mpl
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
import pandas as pd


#%% schedule
schedule = fastf1.get_event_schedule(2023)


# Driver results need this session for scoring
session = fastf1.get_session(2023,'Spielberg','Q')
session.load()
results = session.results # qualifying results 2023 miami gp


top10q = session.results.iloc[0:10].loc[:, ['Abbreviation','Q3']]



# Laps and times 

fastest_lap = session.laps.pick_fastest()
flap = fastest_lap['LapTime']
fdrive = fastest_lap['Driver']



#%% plotting

session.load(telemetry=False, laps=False, weather=False)
Leclerc = session.get_driver('LEC')
print(f"Pronto {Leclerc['FirstName']}?")

fastf1.plotting.setup_mpl()

session.load()
fast_leclerc = session.laps.pick_driver('LEC').pick_fastest()
fast_ver = session.laps.pick_driver('VER').pick_fastest()

ver_car_data = fast_ver.get_car_data()
tver = ver_car_data['Time']
vVer = ver_car_data['Speed']

lec_car_data = fast_leclerc.get_car_data()
t = lec_car_data['Time']
vCar = lec_car_data['Speed']

fig, ax = plt.subplots()

ax.plot(t,vCar,label = 'Leclerc')
ax.plot(tver,vVer,label = 'Verstappen')
ax.set_xlabel('Time')
ax.set_ylabel('Speed [Km/h]')
ax.set_title('Leclerc is')
ax.legend()
plt.show()


# track visualization

year = 2023
wknd = 9
ses = 'Q'
driver = 'VER'
colormap = mpl.cm.plasma

session = ff1.get_session(year,wknd,ses)
weekend = session.event
session.load()
lap = session.laps.pick_driver(driver).pick_fastest()

# get telemetry
x = lap.telemetry['X']
y = lap.telemetry['Y']
color = lap.telemetry['Speed']

points = np.array([x,y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

fig, ax= plt.subplots(sharex=True, sharey=True, figsize=(12,6.75))
fig.suptitle(f'{weekend.name} {year} - {driver} - Speed', size=24, y=.97)

plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)
ax.axis('off')

ax.plot(lap.telemetry['X'], lap.telemetry['Y'], color='black', linestyle='-', linewidth=16, zorder=0)

norm = plt.Normalize(color.min(), color.max())
lc = LineCollection(segments, cmap=colormap, norm=norm, linestyle='-', linewidth=5)

lc.set_array(color)

line = ax.add_collection(lc)

cbaxes = fig.add_axes([0.25, 0.05, 0.5, 0.05])
normlegend = mpl.colors.Normalize(vmin=color.min(), vmax=color.max())
legend = mpl.colorbar.ColorbarBase(cbaxes,norm=normlegend, cmap=colormap, orientation="horizontal")
plt.show()



#%% plotting position change of each driver over a race 

fastf1.plotting.setup_mpl(misc_mpl_mods=False)

session = fastf1.get_session(2023,'Silverstone','R')
session.load(telemetry=False, weather=False)

fig, ax = plt.subplots(figsize=(8.0,4.9))

# 3 letter abbreviation for each driver
d = {}
for drv in session.drivers: # can do for loops through the list nice 
    drv_laps = session.laps.pick_driver(drv)
    
    abb = drv_laps['Driver'].iloc[0] # just indexing 
    color = fastf1.plotting.driver_color(abb)
    ax.plot(drv_laps['LapNumber'], drv_laps['Position'], label=abb, color=color)
    drvlapnumb = drv_laps['LapNumber']
    drvposition = drv_laps['Position']
    # saving the data into an array/dataframe can add more data to have lap times etc...
    dataarray = {'abr': abb, 'Lap Numb': drvlapnumb, 'Pos': drvposition}
    
    # save the data into a dictionary of the dataframes good to manipulate?
    d[drv] = pd.DataFrame(data = dataarray)  
    
    
# answer to manipulation question? https://stackoverflow.com/questions/35717706/python-how-to-turn-a-dictionary-of-dataframes-into-one-big-dataframe-with-colum
    
ax.set_ylim([20.5,0.5])
ax.set_yticks([1,5,10,15,20])
ax.set_xlabel('Lap')
ax.set_ylabel('Position')


ax.legend(bbox_to_anchor=(1.0,1.02))
plt.tight_layout()

plt.show()
    


# dictionary to list
drvlist = [df for df in d.values()]
# large dataframe with the driver name lap number, position, need more data columns added but good method 
drvcombine = pd.concat(drvlist,ignore_index=True)


#%% This cell can be run along with imports to get relevant data and manips.


session = fastf1.get_session(2023,'Silverstone','R') # Q will give all quali.
session.load(telemetry=False, weather=False)
# 3 letter abbreviation for each driver
drvdict = {}
for drv in session.drivers: # can do for loops through the list nice 
    drv_laps = session.laps.pick_driver(drv)
    
    # abb = drv_laps['Driver'].iloc[0] # just indexing 
    # drvlapnumb = drv_laps['LapNumber']
    # drvposition = drv_laps['Position']
    # saving the data into an array/dataframe can add more data to have lap times etc...
    #dataarray = {'abr': abb, 'Lap Numb': drvlapnumb, 'Pos': drvposition}
    dataarray = drv_laps # saves all the data into dictionary
    # dictionary to dynamically save the df in loop ****
    #drvdict[drv] = pd.DataFrame(data = dataarray)  
    drvdict[drv] = pd.DataFrame(data = drv_laps)  

# dictionary to list
drvlist1 = [df for df in drvdict.values()]
# combine the dataframes into a single frame 
drvcombine1 = pd.concat(drvlist1,ignore_index=True)


# Laps and times 

fastest_lap = session.laps.pick_fastest()
flap = fastest_lap['LapTime']
fdrive = fastest_lap['Driver']
