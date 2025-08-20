# -*- coding: utf-8 -*-
"""
Created on Sun Aug 17 19:54:08 2025

@author: Jason
"""

DraftSharks = 'https://www.draftsharks.com/rankings/ppr'
Boone = 'https://sports.yahoo.com/fantasy/article/fantasy-football-rankings-full-ppr-top-300-162244191.html'
Ciely = 'https://www.nytimes.com/athletic/6523411/2025/07/30/fantasy-football-2025-rankings-overall-positional-ppr/' # not PPR by default
FPros = 'https://www.fantasypros.com/nfl/rankings/ppr-cheatsheets.php'
FprosHalf = 'https://www.fantasypros.com/nfl/rankings/half-point-ppr-cheatsheets.php'


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


#%% Boone

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get(Boone)
Boonehtml = driver.page_source
time.sleep(3)
driver.quit()


