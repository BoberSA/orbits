# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 13:54:06 2017

@author: Stanislav
"""
import scipy.optimize
from crtbp_ode import crtbp

def lagrange1(mu):
    #mu2 = 1 - mu
    #a = (mu2/(3*mu))**(1/3)
    #l1 = a-1/3*a**2-1/9*a**3-23/81*a**4
    #return scipy.optimize.root(lambda x:crtbp(0, [x, 0, 0, 0, 0, 0], mu)[3], mu-l1).x
    return scipy.optimize.root(lambda x:crtbp(0, [x, 0, 0, 0, 0, 0], mu)[3], 0.).x[0]

def lagrange2(mu):
    #mu2 = 1 - mu
    #a = (mu2/(3*mu))**(1/3)
    #l2 = a+1/3*a**2-1/9*a**3-31/81*a**4
    #return scipy.optimize.root(lambda x:crtbp(0, [x, 0, 0, 0, 0, 0], mu)[3], mu+l2).x
    return scipy.optimize.root(lambda x:crtbp(0, [x, 0, 0, 0, 0, 0], mu)[3], 2.).x[0]