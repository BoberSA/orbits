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
        mu = mu1 = m1 / (m1 + m2), 
        where m1 and m2 - masses of two main bodies, m1 > m2.

    s0 : array_like with 6 components
        Initial spacecraft state vector (x0,y0,z0,vx0,vy0,vz0).
        
    tspan : array_like with 2 components
        Initial and end time.
        
    Optional
    --------
    
    stopf : function
        Solout function for integrator.
        
    int_param : dict
        Parameters fo 'dopri5' integrator.
        
    Returns
    -------
    
    Yt : np.array
      Array of (n,6) shape of state vectors and times
      for each integrator step (xi,yi,zi,vxi,vyi,vzi,ti)
    
    See Also
    --------
    
    scipy.integrate.ode : Powerfull integrator
    crtbp_ode.crtbp
    
    .. math::
        t_1
    
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

# prop2Planes
# propagates spacecraft in CRTBP described by 'mu' coeff
# until it crosses ('flies by') any of planes:
#   x == planes[0] (event0)
#   x == planes[1] (event1)
#   |y| == planes[2] (event2)
# returns:
#   0 if event1 or event2 occur
#   1 otherwise

def prop2Planes(mu, s0, planes, **kwargs):
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

# propNRevsPlanes
# propagates spacecraft in CRTBP described by 'mu' coeff
# propagates by N revolutions of bounded motion
#
# s0 - initial state vector
# beta - correction angle (in XY plane)
# planes - boundaries (see prop2Planes)
# N - number of revolutions
# dT - period between velocity correction
#       (default: pi, i.e. about one physical revolution)
# dv0 - initial step size
# retDV:
#   if True then additionally return array with all correction dV vectors

def propNRevsPlanes(mu, s0, beta, planes, N=10, dT=np.pi, dv0=0.05, retDV=False, **kwargs):
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