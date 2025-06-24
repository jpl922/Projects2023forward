# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 21:15:51 2025

@author: 17jlo
"""

import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt


teamdata = pd.read_excel('Summary.xlsx')

teampoints = teamdata['P']
teampointpercent = teamdata['P%']
teamshots = teamdata['Shots/GP']

ax1 = teamdata.plot.scatter(x='Shots/GP',y='P',c='Blue')

for idx, row in teamdata.iterrows():
    ax1.annotate(row['Team'], (row['Shots/GP'],row['P']))

ax2 = teamdata.plot.scatter(x='Shots/GP',y='P%',c='Blue')

for idx, row in teamdata.iterrows():
    ax2.annotate(row['Team'], (row['Shots/GP'],row['P%']))
    
    
  