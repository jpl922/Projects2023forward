# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 21:13:18 2024
Chapter 1 SVD from 
Data Driven Science and Engineering (2nd edition)

@author: Jason
"""

#imports
import numpy as np 


#Section 1.1 

#Example 1: SVD 

X = np.random.rand(5,3) # creates random data matrix
U, S, VT = np.linalg.svd(X,full_matrices=True) # Full SVD (Python gives Transpose of V)

Uhat, Shat, VThat = np.linalg.svd(X,full_matrices = False) # economy SVD 


