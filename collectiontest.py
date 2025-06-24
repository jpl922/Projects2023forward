# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 18:55:16 2025
Testing methods for a quick collections tool 


@author: 17jlo
"""

import pandas as pd

# Sample DataFrame (replace this with your actual data import)

TestData = pd.read_excel('ListTests.xlsx')




#grouping data and then .agg which is a dictionary of aggregated data
groupeddata = TestData.groupby('Name').agg({
    "Description":"first",
    "ID": lambda x: list(x)
    }).reset_index()

#aggregating (storing identifiers)
