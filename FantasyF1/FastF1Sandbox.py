# -*- coding: utf-8 -*-
"""
Messing around with FastF1 (plotting, data, and events)
Figure out how to code overtakes

@author: JL_22
"""

# Imports 
import fastf1
import fastf1.plotting
import pandas as pd
from matplotlib import pyplot as plt


schedule = fastf1.get_event_schedule(2023)


session = fastf1.get_session(2023,'United States','Q')
session.load()
results = session.results # qualifying results 2023 miami gp





