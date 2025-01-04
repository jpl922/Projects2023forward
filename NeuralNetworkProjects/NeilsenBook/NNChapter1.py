# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 15:48:32 2025
http://neuralnetworksanddeeplearning.com/chap1.html
Working through Chapter 1 of this book 

Notes: stored in onenote

Goals:
    1. Building a NN from scratch
    2. Improved understanding of Python 
    3. Improved understanding of OOP 
@author: Jason
"""

import random
import numpy as np
#%% Perceptrons 

# hard coding from scratch to understand 

# Network structure inputs (2), L1 (1) L2(2), L3(3)
# parameters: Weights = -2; Bias = 3



# function for a perceptron 

def perceptron(weight,inputs,bias):
    # why does this work? because by default the orperator is checking if the answer is true/false meaning it will return False/True always; int then converts it to 0,1
    return int((np.dot(weight,inputs)+bias) > 0) 
        

def addernetwork(x1,x2):
    b = 3 # bias is constant for all 
    weights = [-2,-2] # all perceptrons have -2 weight and 2 inputs 
    #Layer 1
    p1 = perceptron(weights,[x1,x2],b) # first perceptron
    
    #Layer 2 
    p2 = perceptron(weights,[x1,p1],b) 
    p3 = perceptron(weights,[x2,p1],b)
    
    #Layer 3
    p4sum = perceptron(weights,[p2,p3],b)
    p5carry = perceptron(weights,[p1,p1],b)
    
    return p4sum, p5carry


for i1 in [0,1]:
    for i2 in [0,1]:
        input1 = i1
        input2 = i2
        s,c = addernetwork(input1, input2)
        print(f"{input1} {input2}|  {s}    {c}")
        
# Stopping here, but this does work needed some chatgpt to quickly print the debugging; truth table matches, but don't have the carry bit so only mimics? behavior/half the table    
