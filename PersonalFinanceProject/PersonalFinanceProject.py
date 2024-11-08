# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 21:19:53 2024
SQLLITE
Selenium
polars
seaborn


# credit card does not really matter ally has everything really 

@author: Jason
"""

import polars as pl
import datetime as dt
import sqlite3 
import pandas as pd
import numpy as np




# loading the data starting with just Ally initial
# credit can help with other tracking example grocery costs 
#chase = pd.read_csv("ChaseTransactions.csv")
#capitalone = pd.read_csv("CapitalOneTransactions.csv")
allychecking = pd.read_csv("AllyCheckingtransactions.csv")
allysavings = pd.read_csv("Allysavingstransactions.csv")



# data preprocessing 
# remove extra spaces from column headers
allychecking.columns = allychecking.columns.str.strip()
allysavings.columns = allysavings.columns.str.strip()

ally = pd.merge(allychecking,allysavings, on ="Date")




print(allychecking['Amount'].sum())
print(allysavings['Amount'].sum())












# database
#con = sqlite3.connect("Finances.db")


# 
#ally.to_sql('Ally', con, if_exists ='replace')
#chase.to_sql('Chase',con, if_exists = 'replace')
#capitalone.to_sql('CapitalOne',con,if_exists = 'replace')



#con.close()