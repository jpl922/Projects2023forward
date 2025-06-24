# -*- coding: utf-8 -*-
"""
Created on Mon Jun 23 23:30:28 2025

@author: 17jlo
"""




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










# div = soup.find('div', id='player-bio')
# parts = div.decode_contents().split('<br>')




# for part in parts:
#     text = BeautifulSoup(part, 'html.parser').get_text(strip=True)
#     print(text)



# div = soup.find('div',{'id':'player-bio'})

# lines = list(div.stripped.strings)

# for line in lines:
#     print(line)







    




