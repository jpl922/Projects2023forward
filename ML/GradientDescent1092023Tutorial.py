# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 21:52:42 2023
Gradient Descent from 
https://spin.atomicobject.com/2014/06/24/gradient-descent-linear-regression/
https://github.com/mattnedrich/GradientDescentExample/blob/master/gradient_descent_example.py
Refreshing ML knowledge from MATLAB to Python
@author: 17jlo
"""


# linear regression y = mx+b
# define function 
# approximating y with mx+b and finding error 
# **?, points.y, points.x?
# ** is to the power 

from numpy import *

# Normal discrete error function Sum(yi-mx+b)^2*(1/N)
def computeErrorForLineGivenPoints(b,m,points):
    totalerror = 0 # initializing error
    for i in range(0,len(points)):
        totalError += (points[i].y-(m*points[i].x+b)) ** 2
    return totalError / float(len(points)) 

# gradients partial derivatives for m and b for error function
# raised to power simple partial derivative just forget lol



def stepGradient(b_current,m_current, points, learningRate):
    b_gradient = 0; # init
    m_gradient = 0; # init
    N = float(len(points))
    for i in range(0,len(points)):
        b_gradient += (2/N) * (points[i].y-((m_current*points[i].x)+b_current))
        m_gradient += (2/N) * points[i].x * (points[i].y-((m_current*points[i].x)+b_current))
        new_b = b_current - (learningRate*b_gradient) # LR = step sizes down
        new_m = m_current - (learningRate*m_gradient)
        return [new_b, new_m]
    
    
    
    
