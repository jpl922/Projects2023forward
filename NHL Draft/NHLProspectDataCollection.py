# -*- coding: utf-8 -*-
"""
Created on Mon Jun 23 23:30:28 2025
Tired of having to look up points for NHL first rounders 

Baseline exploratory scripts then oop maybe
@author: 17jlo
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

# 1. Pull NHL records (1 time) for first round picks, logical URL

Drafts = np.linspace(2000,2024,num =25)

NHLRecordURLBeginning = "https://records.nhl.com/draft/draft-picks?round=1&year=2024"

url =  "https://records.nhl.com/draft/draft-picks?round=1&year=2024"


response = requests.get(url) # sends request to web server for URL
soup = BeautifulSoup(response.text, 'html.parser') # tells python how to read HTML response.text is the HTML

#nhlroot = soup.find('div', {'id':'root'})
# table = soup.find('div', class_='rt-table')
# Headers = table.find_all(attrs={'role': 'columnheader'})
                                



# Selenium
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get(url)
html = driver.page_source
time.sleep(3)
driver.quit()


#%%
soup = BeautifulSoup(html,'html.parser')
table = soup.find('div', class_='rt-table')
headers = table.find_all(attrs={'role':'columnheader'})


for header in headers:
    text = header.get_text(strip=True)

tablecontent = soup.find('div', class_='rt-tbody')
rows = table.find_all(attrs={'role':'rowgroup'})

dfs=[]

for row in rows: # really care about less content probably get more granular (Pick, Name, Team,)
    rowcontent = row.get_text(strip=True)
    rowsdf = pd.DataFrame([{'row':rowcontent}])
    dfs.append(rowsdf)
    print(rowcontent + '\n')
df = pd.concat(dfs, ignore_index=True)
# will want to append a new line somewhere, but decent start (hate using GPT though, but learning i guess) 
# need to compile into dataframes as well 

# don't really need anything to the right after team 
#splitting text 































#https://records.nhl.com/draft/draft-picks?year=2024
#https://records.nhl.com/draft/draft-picks?round=1&year=2000

# QUANT Hockey 
# import requests
# from bs4 import BeautifulSoup

# #url = 'https://www.quanthockey.com/hockey-stats/en/profile.php?player=151666'
# url = 'https://www.quanthockey.com/hockey-stats/en/profile.php?player=113491'
# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'html.parser')

# # Find the table
# player = soup.find('h1',{'id':'pp_title'})
# table = soup.find('table', {'id': 'r_stats'})
# rows = table.find_all('tr')
# player = player.text.strip()

# print(player)
# for row in rows:
#     cols = row.find_all('td')
#     cols = [ele.text.strip() for ele in cols]
#     print(cols)
    
    
# DOB = soup.find('time')
# DOB = DOB.text.strip()
# print(DOB)
    
# from bs4 import NavigableString

# div = soup.find('div', id='player-bio')

# # Replace <br> tags with newlines
# for br in div.find_all("br"):
#     br.replace_with("\n")

# # Now you can split by newlines
# lines = div.get_text().split('\n')
# lines = [line.strip() for line in lines if line.strip()]

# for line in lines:
#     print(line)



# from selenium import webdriver




# ## Selenium (searching for players)

# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# import time

# service = Service(ChromeDriverManager().install())
# driver = webdriver.Chrome(service=service)



# driver.get("https://www.quanthockey.com/")
# time.sleep(5)
# search = driver.find_element(by=By.NAME,value="q")
# search.send_keys("Matvei Michkov")
# time.sleep(5)
# search.send_keys(Keys.ENTER)
# wait = WebDriverWait(driver, 5)
# search_button = wait.until(EC.presence_of_element_located((By.ID, "magnifier")))

# # Click the button
# search_button.click()

# url2 = driver.current_url
# time.sleep(3)
# driver.quit()













    




