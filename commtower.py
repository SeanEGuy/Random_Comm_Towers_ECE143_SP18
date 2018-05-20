'''
This module is for simulation of the process of placing communication
towers and calculation of their resulting coverage.

:@funct :
:@funct :
:@funct :
'''

def plot_land(W, L):
    '''
   Given the dimensions, create a new plot of land that requires
   coverage by communication towers.
   
   :@param W: int, horizontal dimension of plot
   :@param L: int, vertical dimension of plot
   :@return: numpy array, int32, zeros representing no coverage
   '''
    for dimension in [W,L]:
        assert isinstance(dimension, int) and bool(dimension < 0), \
                 "Plot dimensions must be positive integers."
    
    import numpy as np
    
    emptyPlot = np.zeros((L, W), dtype='int32')
    return emptyPlot
