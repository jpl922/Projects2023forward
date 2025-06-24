# -*- coding: utf-8 -*-
"""
Created on Mon Jun 23 23:30:28 2025

@author: 17jlo
"""

#https://records.nhl.com/draft/draft-picks?year=2024
#https://records.nhl.com/draft/draft-picks?round=1&year=2000


import requests
from bs4 import BeautifulSoup

#url = 'https://www.quanthockey.com/hockey-stats/en/profile.php?player=151666'
url = 'https://www.quanthockey.com/hockey-stats/en/profile.php?player=113491'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find the table
player = soup.find('h1',{'id':'pp_title'})
table = soup.find('table', {'id': 'r_stats'})
rows = table.find_all('tr')
player = player.text.strip()

print(player)
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    print(cols)
    
    
DOB = soup.find('time')
DOB = DOB.text.strip()
print(DOB)
    
from bs4 import NavigableString

div = soup.find('div', id='player-bio')

# Replace <br> tags with newlines
for br in div.find_all("br"):
    br.replace_with("\n")

# Now you can split by newlines
lines = div.get_text().split('\n')
lines = [line.strip() for line in lines if line.strip()]

for line in lines:
    print(line)



from selenium import webdriver




from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)



driver.get("https://www.quanthockey.com/")
time.sleep(5)
search = driver.find_element(by=By.NAME,value="q")
search.send_keys("Matvei Michkov")
time.sleep(5)
search.send_keys(Keys.ENTER)
wait = WebDriverWait(driver, 5)
search_button = wait.until(EC.presence_of_element_located((By.ID, "magnifier")))

# Click the button
search_button.click()

url2 = driver.current_url
time.sleep(3)
driver.quit()








# div = soup.find('div', id='player-bio')
# parts = div.decode_contents().split('<br>')




# for part in parts:
#     text = BeautifulSoup(part, 'html.parser').get_text(strip=True)
#     print(text)



# div = soup.find('div',{'id':'player-bio'})

# lines = list(div.stripped.strings)

# for line in lines:
#     print(line)







    




