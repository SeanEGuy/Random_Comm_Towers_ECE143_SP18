'''
This module is for simulation of the process of placing communication
towers and calculation of their resulting coverage.

:@funct :
:@funct :
:@funct :
'''

def plot_land(L, W):
    '''
   Given the dimensions, create a new plot of land that requires
   coverage by communication towers.
   
   The module numpy must be available for this function to work.
   
   This function has two primary purposes. First it passes W and L, the
   user inputs for width and length of the plot of land to be
   populated with communication towers, through an assert statement.
   This checks that W and L are positive (n>0) integers.
   
   Then the function imports the numpy module before generating a
   two-dimensional array of zeros with L rows and W values in each row.
   The zeros themselves are 32-bit integers.
   
   :@param W: int, horizontal dimension of plot
   :@param L: int, vertical dimension of plot
   :@return: numpy array, int32, zeros representing no coverage
   '''
    for dimension in [W, L]:
        assert isinstance(dimension, int) and bool(dimension > 0), \
                 "Plot dimensions must be positive integers."
    
    try:
        import numpy
    except:
        print "numpy module not found." #checking for numpy module
    
    import numpy as np
    emptyPlot = np.zeros((L, W), dtype='int32') #generate output array
    
    return emptyPlot


def place_tower(plotArray)
    '''
   Places a random rectangle representing one tower's coverage in a
   given plot of land.
   
   :@param plotArray: numpy array, dimensions represnting a plot of land
   :@return: tuple, coordinates of a rectangle in the plot
   '''
    
    assert