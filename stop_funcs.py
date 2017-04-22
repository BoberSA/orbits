# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 13:55:16 2017

@author: Stanislav
"""

import numpy as np
import math

def stopNull(t, s, lst):
    lst.append(np.hstack((s,t)))
    return 0

def stopY0m(t, s, lst):
    lst.append(np.hstack((s,t)))
    if (s[1] < 0):
        return -1
    return 0

def stopPlanes(t, s, lst, **kwargs):
    lst.append(np.hstack((s,t)))
    if ((s[0] < kwargs['planes'][0]) or (s[0] > kwargs['planes'][1])):
        return -1
    return 0

def stop3Planes(t, s, lst, **kwargs):
    lst.append(np.hstack((s,t)))
    if ((s[0] < kwargs['planes'][0]) or (s[0] > kwargs['planes'][1]) or (math.fabs(s[1]) > kwargs['planes'][2])):
        return -1
    return 0