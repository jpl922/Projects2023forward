# -*- coding: utf-8 -*-
"""
Compiling rankings just want to extract and store rankings with the player

@author: 17jlo
"""

import pandas as pd

df = pd.read_excel(r'C:\Users\17jlo\Desktop\Ryan_8_27_draft prep.xlsx', sheet_name='compiled')
print(df)


dfFP = df[['FP Player', 'FP Rank']]
dfBoone = df[['Boone Player','Boone Rank']]
dfDS = df[['DS Player','DS Rank']]
dfWaz = df[['Waz Player','Waz Rank']]
# Rename the column
new_column_name = 'Player'
dfFP.rename(columns={'FP Player': new_column_name}, inplace=True)
dfBoone.rename(columns={'Boone Player': new_column_name}, inplace=True)
dfDS.rename(columns={'DS Player': new_column_name}, inplace=True)
dfWaz.rename(columns={'Waz Player': new_column_name}, inplace=True)


PlayerwithRank = dfFP.merge(dfBoone, on='Player', how='outer').merge(dfDS, on='Player', how='outer').merge(dfWaz, on='Player', how='outer')

PlayerwithRank['Average'] = PlayerwithRank[['FP Rank', 'Boone Rank', 'DS Rank','Waz Rank']].mean(axis=1)
