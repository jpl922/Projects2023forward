# -*- coding: utf-8 -*-
"""
Created on Sun Aug 17 19:54:08 2025

@author: Jason
"""



#Imports

#Manipulation
import pandas as pd
import numpy as np 
import matplotlib as mpl
import seaborn as sb # might not use 

#Scraping
import requests
from bs4 import BeautifulSoup


#Selenium (Quant)
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

import os



# init Selenium
service = Service(ChromeDriverManager().install())  # need to look into if one time setup or every time
driver = webdriver.Chrome(service=service) # driver is basically the chromium browser functions


#URLs

Boone = 'https://sports.yahoo.com/fantasy/article/fantasy-football-rankings-full-ppr-top-300-162244191.html'
Ciely = 'https://www.nytimes.com/athletic/6523411/2025/07/30/fantasy-football-2025-rankings-overall-positional-ppr/' # not PPR by default
FPros = 'https://www.fantasypros.com/nfl/rankings/ppr-cheatsheets.php'
#FprosHalf = 'https://www.fantasypros.com/nfl/rankings/half-point-ppr-cheatsheets.php'



#Yahoo; data is stored in a wrapper
#https://stackoverflow.com/questions/5585343/getting-the-return-value-of-javascript-code-in-selenium/5585345#5585345



#draft sharks
# <tbody data-player-row data-key= value
#<table class="table sort-numerical dynasty-rankings" id="rankingsTable" x-ref="rankingsTable">

# athletic

#can just download, but otherwise need to get it to change to PPR
#div id = "fp-widget-body">

# selection for PPR
# select id = "fp-widget-pos-seelct ; value = PPR 

# fantasy pros
# tbody 


#%% Acquire HTML (might not need)

# driver.get(Boone) # go to URL
# Boonehtml = driver.page_source # grab page HTML
# time.sleep(15) # prevent from closing too fast

# time.sleep(3)
# driver.get(Ciely)
# Cielyhtml = driver.page_source
# time.sleep(3)
# driver.get(FPros)
# FPhtml = driver.page_source
# time.sleep(3)
#driver.quit() # close browser


#%% Boone
# driver.get(Boone) # go to URL
# Boonehtml = driver.page_source # grab page HTML
# time.sleep(15) # prevent from closing too fast
#BooneSoup = BeautifulSoup(Boonehtml,"html.parser")
#Datawrapper = BooneSoup.find_all('iframe')

# Steps to get data 
#1. inspect page
#2. find datawrapper
#3. add data.csv to end of link 
BooneWrapper = 'https://datawrapper.dwcdn.net/Of2id/8/data.csv'
BooneData = pd.read_csv(BooneWrapper, index_col=False)



#%% Ciely/Fpros (download buttons)
# Just download the files? (very easy)
CielyData = pd.read_csv(r"C:\Users\Jason\Desktop\Hobby\Programming\Projects2023forward\FFRankings\2025_Data\Ciely20258_25.csv", index_col=False) # need to clean file (remove top label)
FProsData = pd.read_csv(r"C:\Users\Jason\Desktop\Hobby\Programming\Projects2023forward\FFRankings\2025_Data\FPros20258_25.csv", index_col=False)



#%% DraftSharks (probably actually worth scraping)
DraftSharks = 'https://www.draftsharks.com/rankings/ppr'
driver.get(DraftSharks)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

time.sleep(2)
DShtml = driver.page_source
time.sleep(2)
driver.quit()
#response = requests.get(DraftSharks)
soup = BeautifulSoup(DShtml, 'html.parser')


# need to strip smarter don't need all the 

# Find the table
ColumnHeader = soup.find_all('th')
PlayerRows = soup.find_all('tr',class_="player-row")
Names = soup.find_all('a',class_="hide-on-mobile")
Positions = soup.find_all('div',class_="position-rank RB")

data=[]
for row in PlayerRows:
    cells = [cell.get_text(strip=True) for cell in row.find_all("td")]
    data.append(cells)

player_names = [Name.get_text(strip=True) for Name in Names] # gets names correctly
Position_Ranks = [Position.get_text(strip=True) for Position in Positions]

Columns = ['RK','Team','Player','Pos','Games','ADP','Bye','SOS','Injury Risk','Floor Proj','Consens Proj','DS Proj','Ceiling Proj','3D value']

DSdata = pd.DataFrame(data,columns=Columns)
DSdata["Player"] = player_names
DSdata['Pos'] = Position_Ranks

#POS to remove LB; DL, DB

DSDataClean = DSdata[~DSdata.Pos.str.contains("LB|DL|DB")] # think this works maybe for wrong reason, but IDK 
DSDataClean = DSDataClean[DSDataClean.index <=309]
DSDataClean["RK"] = pd.to_numeric(DSDataClean["RK"], errors="coerce")
#%% Renaming columns 
BooneData = BooneData.rename(columns={'Rank':'Boone Rank'})
FProsData = FProsData.rename(columns={'RK':'FPros Rank','PLAYER NAME':'Player','TIERS':'FPros Tiers'})
CielyData = CielyData.rename(columns={'Player Name':'Player','Rank':'Ciely Rank'})
DSdf = DSDataClean.rename(columns={'RK':'DS Rank','ADP':'DS ADP'})

DSdf["Player"] = DSdf["Player"].replace({"Aaron Jones":"Aaron Jones Sr.",
"Cameron Skattebo":"Cam Skattebo",
"Cameron Ward":"Cam Ward",
"Chigoziem Okonkwo":"Chig Okonkwo",
"Chris Rodriguez": "Chris Rodriguez Jr.",
"D.J. Moore": "DJ Moore",
"D.K. Metcalf":"DK Metcalf",
"Deebo Samuel": "Deebo Samuel Sr.",
"Kyle Pitts":"Kyle Pitts Sr.",
"Patrick Mahomes":"Patrick Mahomes II",
"Travis Etienne":"Travis Etienne Jr.",
"Tre Harris":"Tre' Harris"})


CompiledDF = FProsData.merge(BooneData, on = "Player", how="outer").merge(CielyData, on = "Player", how="outer").merge(DSdf, on="Player", how="outer")

FFRanks = CompiledDF[["Player","POS","TEAM","Boone Rank", "Ciely Rank","DS Rank", "FPros Rank","BYE","SOS_x","Injury Risk","DS ADP", "FPros Tiers"]]

FFRanks['Avg Rank'] = FFRanks[['DS Rank', 'Boone Rank', 'Ciely Rank']].mean(axis=1)

FFRanks.to_excel('2025FFRankings.xlsx',index=False)
