# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 13:58:00 2017

@author: Stanislav
"""

import numpy as np
import scipy, math
from crtbp_ode import crtbp
from stop_funcs import stopNull

def propCrtbp(mu, s0, tspan, **kwargs):
    ''' Propagate spacecraft in CRTBP.
        Uses scipy.integrate.ode with 'dopri5' integrator.
    
    Parameters
    ----------
    mu : scalar
        CRTBP mu1 coefficient.

    s0 : array_like with 6 components
        Initial spacecraft state vector (x0,y0,z0,vx0,vy0,vz0).
        
    tspan : array_like with 2 components
        Initial and end time.
        
    Optional
    --------
    
    stopf : function
        Solout function for integrator.
        
    int_param : dict
        Parameters for 'dopri5' integrator.
        
    Returns
    -------
    
    Yt : np.array
      Array of (n,6) shape of state vectors and times
      for each integrator step (xi,yi,zi,vxi,vyi,vzi,ti)
    
    See Also
    --------
    
    scipy.integrate.ode, crtbp_ode.crtbp
       
    '''
    prop = scipy.integrate.ode(crtbp)
    prop.set_initial_value(s0, tspan[0])
    prop.set_f_params(*[mu])
    if 'int_param' in kwargs:
        prop.set_integrator('dopri5', **kwargs['int_param'])
    else:
        prop.set_integrator('dopri5')
    lst = []
    #print(kwargs)
    if 'stopf' in kwargs:
        prop.set_solout(lambda t, s: kwargs['stopf'](t, s, lst, **kwargs))
    else:
        prop.set_solout(lambda t, s: stopNull(t, s, lst))
    prop.integrate(tspan[1])
    return np.asarray(lst)


def prop2Planes(mu, s0, planes, **kwargs):
    ''' Propagate spacecraft in CRTBP up to defined terminal planes.
        Uses scipy.integrate.ode with 'dopri5' integrator.
    
    Parameters
    ----------
    mu : scalar
        CRTBP mu1 coefficient.

    s0 : array_like with 6 components
        Initial spacecraft state vector (x0,y0,z0,vx0,vy0,vz0).
        
    planes : array_like with 3 components
        planes[0] defines terminal plane x == planes[0],
        planes[1] defines terminal plane x == planes[1],
        planes[2] defines 2 terminal planes
            |y| == planes[2].
         
    Optional
    --------
    
    **kwargs : dict
        Parameters for 'dopri5' integrator.
        
    Returns
    -------
    
    0 : if spacecraft crosses plane[0]
    1 : otherwise
    
    See Also
    --------
    
    scipy.integrate.ode, crtbp_ode.crtbp
       
    '''

    def _stopPlanes(t, s, planes=planes):
        if ((s[0] < planes[0]) or (s[0] > planes[1]) or (math.fabs(s[1]) > planes[2])):
            return -1
        return 0
    prop = scipy.integrate.ode(crtbp)
    prop.set_initial_value(s0, 0)
    prop.set_f_params(*[mu])
    prop.set_integrator('dopri5', **kwargs)
    prop.set_solout(lambda t, s:_stopPlanes(t, s, planes))
    s1 = prop.integrate(3140.0)
    if ((s1[0] > planes[1]) or (math.fabs(s1[1]) > planes[2])):
        return 1
    return 0

from find_vel import findVPlanes


def propNRevsPlanes(mu, s0, beta, planes, N=10, dT=np.pi, dv0=0.05, retDV=False, **kwargs):
    ''' Propagate spacecraft in CRTBP for N revolutions near libration point.
        Every dT period calculates velocity correction vector at beta angle
        (findVPlanes) for bounded motion. Initial beta = 90 degrees and
        initial velocity correction vector is velocity itself. 
        Uses propCrtbp, findVPlanes.
    
    Parameters
    ----------
    mu : scalar
        mu = mu1 = m1 / (m1 + m2), 
        where m1 and m2 - masses of two main bodies, m1 > m2.

    s0 : array_like with 6 components
        Initial spacecraft state vector (x0,y0,z0,vx0,vy0,vz0).
        
    beta : angle at which corrections will be made.
        
    planes : array_like with 3 components
        planes[0] defines terminal plane x == planes[0],
        planes[1] defines terminal plane x == planes[1],
        planes[2] defines 2 terminal planes
            |y| == planes[2].
            
    N : scalar
        Number of revolutions.

    dT : scalar
        Time between velocity corrections.
        (default: pi, i.e. about one spacecraft revolution)

    dv0 : scalar
        Initial step for correction calculation.

    retDV : boolean
        If True then additionally returns array with all
        correction dV vectors.    
         
    Optional
    --------
    
    **kwargs : dict
        Parameters for propCrtbp and findVPlanes.
        
    Returns
    -------
    
    arr : np.array
      Array of (n,6) shape of state vectors and times
      for each integrator step (xi,yi,zi,vxi,vyi,vzi,ti)
    
    DV : np.array
        Array of (N,) shape with correction values.
        (only if retDV is True)
    
    See Also
    --------
    
    propCrtbp, findVPlanes
       
    '''

    v = findVPlanes(mu, s0, 90, planes, dv0, **kwargs)
    s1 = s0.copy()
    s1[3:5] += v
    DV = v.copy()
    cur_rev = propCrtbp(mu, s1, [0, dT], **kwargs)
    arr = cur_rev.copy()
    print(0, end=' ')
    for i in range(N-1):
        s1 = arr[-1, :-1].copy()
        v = findVPlanes(mu, s1, beta, planes, dv0, **kwargs)
        s1[3:5] += v
        cur_rev = propCrtbp(mu, s1, [0, dT], **kwargs)
        arr = np.vstack((arr, cur_rev[1:]))
        DV = np.vstack((DV, v))
        print(i+1, end=' ')
    if retDV:
        return arr, DV
    return arr