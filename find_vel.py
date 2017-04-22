# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 14:16:34 2017

@author: Stanislav
"""

import math
import numpy as np
from crtbp_prop import prop2Planes

# findVPlanes
# uses special version of bisection method and plane boundaries to calculate
# velocity correction vector for spacecraft bounded motion
# near unstable lagrange points in CRTBP described by 'mu' coeff;
#
# s0 - initial state vector
# beta - correction angle (in XY plane)
# planes - boundaries (see prop2Planes)
# dv0 - initial step size
#
# returns dV = [dVx, dVy] - velocity correction vector

def findVPlanes(mu, s0, beta, planes, dv0, **kwargs):
    s1 = np.asarray(s0).copy()
    vstart = s1[3:5].copy()
    dv = dv0
    dvtol = kwargs.get('dvtol', 1e-16)
    
    
    rads = math.radians(beta)
    beta_n = np.array([math.cos(rads), math.sin(rads)])
    
    p = prop2Planes(mu, s1, planes, **kwargs)
    if p == 1:
        dv = -dv
        
    v = dv

    while math.fabs(dv) > dvtol:
        s1[3:5] = vstart + v * beta_n
        p1 = prop2Planes(mu, s1, planes, **kwargs)
     
        if p1 != p:
            v -= dv
            dv *= 0.5

        v += dv
        
    return v * beta_n