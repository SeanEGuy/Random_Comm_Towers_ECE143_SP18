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


def make_random_tower(plotArray)
    '''
   Generates a random rectangle representing one tower's coverage in a
   given plot of land. Ignores rules of overlapping and trimming.
   
   :@param plotArray: numpy array, dimensions represnting a plot of land
   :@return: tuple, coordinates of a rectangle in the plot
   '''
    import numpy as np
    import 
    
    assert isinstance(plotArray, np.ndarray) \ #check if a numpy array
             and bool(len(plotArray.shape) == 2), \ #check two dimensions
             "Input must be a two-dimensional numpy array."
    
    L, W = plotArray.shape #save row number as L and cols as W
    
    rectW = list( np.random.randint(0, W, 2) )
    rectL = list( np.random.randint(0, L, 2) )
    #picks two values per dimension, determines coverage length & width
    rectW.sort()
    rectL.sort()
    #sort coordinates in an increasing order
    
    rectRange = tuple( rLength + rWidth )
    #Combine coords in pattern of (x1, x2, y1, y2)
    assert bool(len(rDimensions) == 4) #Checking shape of output
    
    rectPlot = plotArray * 0 #zero int array of same dimensions
    
    iterPlot = np.nditer(coverPlot, flags=['multi_index'], op_flags=['writeonly'])
    #Make iterable version of input plot array
    #Flag args provide multiple indices and permits writing in data
    while not iterPlot.finished: #loop through each element in array
        i,j = iterPlot.multi_index #save indices in i & j
        if rectRange[0] <= i <= rectRange[1] \
            and rectRange[2] <= j <= rectRange[3]:
            #testing for each position if in tower coverage
            iterPlot[0] = 1 #If in range, change value to a one
        iterPlot.iternext() #moves to next element in array
    
    assert bool(rectPlot.shape == plotArray.shape)
    #final array output should be the same shape as the input
    return rDimensions

    
    
    