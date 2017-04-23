# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 14:39:12 2017

@author: Stanislav
"""

import matplotlib.pyplot as plt

def plot3Proj(arr, size=(15,5), **kwargs):
    ''' Plot 3 projections (XY, XZ, YZ) of trajectory in one figure.
        _
    
    Parameters
    ----------

    arr : np.array
        Array of shape (n,k), where k >= 3 that consists of trajectory points.
               
    Optional
    --------
    
    col : dict
        Should be as {0:XY_color, 1:XZ_color, 2:YZ_color}
        *_color format is like plt.plot can use. 
    
    scale : scalar
        Scale coefficient for coordinates. Can be useful for coordinate
        scaling from dimensionless values to dimensioned (ex. kilometers).
    
    plot_param : dict
        Parameters for plt.plot function.
        
    Returns
    -------
    
    fig : plt.figure
        Figure consists of 3 axis with corresponding projections drawn
        on them.
          
    '''
    fig, ax = plt.subplots(1, 3)
    fig.set_size_inches(size)
    lbl = {0: '$X$', 1: '$Y$', 2: '$Z$'}
    col = kwargs.get('col', {0: 'red', 1: 'green', 2: 'blue'})
    axs = {0: (0, 1), 1: (0, 2), 2: (1, 2)}
    s = kwargs.get('scale', 1.0)
    
    for i in range(3):
        if 'plot_param' in kwargs:
            ax[i].plot(arr[:, axs[i][0]]*s, arr[:, axs[i][1]]*s, col[i], **kwargs['plot_param'])
        else:
            ax[i].plot(arr[:, axs[i][0]]*s, arr[:, axs[i][1]]*s, col[i])
        ax[i].set_xlabel(lbl[axs[i][0]] + kwargs.get('dim', ''))
        ax[i].set_ylabel(lbl[axs[i][1]] + kwargs.get('dim', ''))
        ax[i].set_aspect('equal', 'datalim')
        
    fig.tight_layout()
    return fig

def plot3Proj_adv(arrs, size=(15,5), **kwargs):
    ''' Plot 3 projections (XY, XZ, YZ) of number of \
        trajectories in one figure.
        _
    
    Parameters
    ----------

    arrs : array_like of np.arrays 
        arrs consist of np.arrays same as in plot3Proj function
               
    Optional
    --------
    
    col : dict
        Should be as {0:XY_color, 1:XZ_color, 2:YZ_color}.
        *_color format is like plt.plot can use. 
    
    scale : scalar
        Scale coefficient for coordinates. Can be useful for coordinate
        scaling from dimensionless values to dimensioned (ex. kilometers).
    
    plot_param : dict
        Parameters for plt.plot function.
        
    Returns
    -------
    
    fig : plt.figure
        Figure consists of 3 axis with corresponding projections drawn
        on them.
        
    See Also
    --------
    
    plot3Proj.
          
    '''
    fig, ax = plt.subplots(1, 3)
    fig.set_size_inches(size)
    lbl = {0: '$X$', 1: '$Y$', 2: '$Z$'}
    col = kwargs.get('col', {0: 'red', 1: 'green', 2: 'blue'})
    axs = {0: (0, 1), 1: (0, 2), 2: (1, 2)}
    s = kwargs.get('scale', 1.0)
    
    for i in range(3):
        if 'plot_param' in kwargs:
            for arr in arrs: 
                ax[i].plot(arr[:, axs[i][0]]*s, arr[:, axs[i][1]]*s, col[i], **kwargs['plot_param'])
        else:
            for arr in arrs: 
                ax[i].plot(arr[:, axs[i][0]]*s, arr[:, axs[i][1]]*s, col[i])
        ax[i].set_xlabel(lbl[axs[i][0]] + kwargs.get('dim', ''))
        ax[i].set_ylabel(lbl[axs[i][1]] + kwargs.get('dim', ''))
        ax[i].set_aspect('equal', 'datalim')
        
    fig.tight_layout()
    return fig