# -*- coding: utf-8 -*-
"""
Created on Tue Nov 18 20:03:05 2025
Chapter 1 Singular Value Decomposition 
@author: Jason
"""

# Imports
import numpy as np 

# Section 1.1 SVD in Python
X = np.random.rand(5,3) # 5x3 random matrix 
U, S, VT = np.linalg.svd(X,full_matrices=True) # Full SVD; outputs transpose V
Uhat, Shat, VThat = np.linalg.svd(X, full_matrices=False) # economy SVD



