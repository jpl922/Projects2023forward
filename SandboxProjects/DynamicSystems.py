# -*- coding: utf-8 -*-
"""
Created on Fri Nov 14 22:17:46 2025

@author: Jason
"""

%matplotlib nbagg
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import odeint

l = 1 # m
g = 9.81 #m/s^2

def f(X,t):
    