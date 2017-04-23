# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 13:55:16 2017

@author: Stanislav
"""

import numpy as np
import math

def stopNull(t, s, lst):
    ''' Dummy function for scipy.integrate.ode solout application. \
        Can be used for gathering all intergation steps.
        Shoudn't be called directly but through scipy.integrate.ode.
    
    Parameters
    ----------

    t : scalar
        Dimensionless time (same as angle of system rotation).
        
    s : array_like with 6 components
        State vector of massless spacecraft (x,y,z,vx,vy,vz)

    lst : list
        Every call of this function put np.hstack of (s, t) into lst. 
                      
    Returns
    -------
    
    0 : scalar
        Always. Will be treated by scipy.integrate.ode as it shouldn't
        stop integration process.
          
    '''
    lst.append(np.hstack((s,t)))
    return 0

def stopY0m(t, s, lst):
    ''' Solout function for scipy.integrate.ode. Stops integration \
        when Y coordinate of spacecraft becomes lower than zero.
        Also can be used for gathering all intergation steps.
        Shoudn't be called directly but through scipy.integrate.ode.
    
    Parameters
    ----------

    t : scalar
        Dimensionless time (same as angle of system rotation).
        
    s : array_like with 6 components
        State vector of massless spacecraft (x,y,z,vx,vy,vz)

    lst : list
        Every call of this function put np.hstack of (s, t) into lst. 
                      
    Returns
    -------
    
    -1 : scalar
        If Y coordinate of spacecraft < 0. Will be treated by
        scipy.integrate.ode as it should stop integration process.
        
    0 : scalar
        Otherwise. Will be treated by scipy.integrate.ode as it should NOT
        stop integration process.
          
    '''
    lst.append(np.hstack((s,t)))
    if (s[1] < 0):
        return -1
    return 0

def stopPlanes(t, s, lst, **kwargs):
    ''' Solout function for scipy.integrate.ode. Stops integration \
        when spacecraft reaches any of 2 planes.
        Also can be used for gathering all intergation steps.
        Shoudn't be called directly but through scipy.integrate.ode.
    
    Parameters
    ----------

    t : scalar
        Dimensionless time (same as angle of system rotation).
        
    s : array_like with 6 components
        State vector of massless spacecraft (x,y,z,vx,vy,vz)

    lst : list
        Every call of this function put np.hstack of (s, t) into lst. 
        
    planes : array_like of 2 scalars
        Defines planes x == planes[0] and x == planes[1] which crossing
        by spacecraft will stop integration.
        
                      
    Returns
    -------
    
    -1 : scalar
        When spacecraft reaches planes. Will be treated by
        scipy.integrate.ode as it should stop integration process.
        
    0 : scalar
        Otherwise. Will be treated by scipy.integrate.ode as it should NOT
        stop integration process.
                 
    '''
    lst.append(np.hstack((s,t)))
    if ((s[0] < kwargs['planes'][0]) or (s[0] > kwargs['planes'][1])):
        return -1
    return 0

def stop3Planes(t, s, lst, **kwargs):
    ''' Solout function for scipy.integrate.ode. Stops integration \
        when spacecraft reaches any of 3 planes.
        Also can be used for gathering all intergation steps.
        Shoudn't be called directly but through scipy.integrate.ode.
    
    Parameters
    ----------

    t : scalar
        Dimensionless time (same as angle of system rotation).
        
    s : array_like with 6 components
        State vector of massless spacecraft (x,y,z,vx,vy,vz)

    lst : list
        Every call of this function put np.hstack of (s, t) into lst. 
        
    planes : array_like of 3 scalars
        Defines planes x == planes[0], x == planes[1] and
        |y| == planes[2] which crossing by spacecraft will stop integration.

    Returns
    -------
    
    -1 : scalar
        When spacecraft reaches planes. Will be treated by
        scipy.integrate.ode as it should stop integration process.
        
    0 : scalar
        Otherwise. Will be treated by scipy.integrate.ode as it should NOT
        stop integration process.
        
    See Also
    --------
    
    crtbp_prop.prop2Planes.
          
    '''
    lst.append(np.hstack((s,t)))
    if ((s[0] < kwargs['planes'][0]) or (s[0] > kwargs['planes'][1]) or (math.fabs(s[1]) > kwargs['planes'][2])):
        return -1
    return 0