# -*- coding: utf-8 -*-
"""
Created on Tue Nov 18 20:03:05 2025
Chapter 1 Singular Value Decomposition 
@author: Jason
"""
 

#Imports cross section
import numpy as np 
import os
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [16, 8]

# Section 1.1 SVD in Python

X = np.random.rand(5,3) # 5x3 random matrix 
U, S, VT = np.linalg.svd(X,full_matrices=True) # Full SVD; outputs transpose V
Uhat, Shat, VThat = np.linalg.svd(X, full_matrices=False) # economy SVD

# Section 1.2 Example Image Compression different code on site

from matplotlib.image import imread
A = imread(os.path.join('DATA','LisbonWallPaper.jpg'))
X = np.mean(A, -1) # Convert RGB to grayscale (removes 3rd column)
img = plt.imshow(X)
img.set_cmap('gray') # github 
plt.axis('off')
plt.show()

# Compute the SVD
U, S, VT = np.linalg.svd(X,full_matrices=False) # economy
S = np.diag(S)
j=0 #github
# approximate matrix with truncated SVD for various ranks r
for r in (5,20,100,500): # create approximate images
    Xapprox = U[:,:r] @ S[0:r,:r] @ VT[:r,:] # @ is matrix multiplication r col, rxr, 4 r rows
    plt.figure(j+1)
    j+=1
    img = plt.imshow(Xapprox)
    img.set_cmap('gray') # github 
    plt.axis('off')
    plt.title('r= ' +str(r))
    plt.show()

    
# Plot singular values and cumulative sum
plt.figure(1)
plt.semilogy(np.diag(S))
plt.figure(2)
plt.plot(np.cumsum(np.diag(S))/np.sum(np.diag(S)))
