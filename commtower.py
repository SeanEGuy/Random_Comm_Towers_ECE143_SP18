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


def make_random_tower(plotArray):
    '''
    Generates a random rectangle representing one tower's coverage in a
    given plot of land. Ignores rules of overlapping and trimming.
    
    :@param plotArray: numpy array, dimensions representing plot of land
    :@return: numpy array, plot with coverage mapped out
    '''
    import numpy as np #used for arrays and random integers
    
    assert isinstance(plotArray, np.ndarray), \
           "Input must be a two-dimensional numpy array."
           #check if a numpy array
    assert bool(len(plotArray.shape) == 2), \
           "Input must be a two-dimensional numpy array."
           #check if 2-D
    
    L, W = plotArray.shape #save row number as L and cols as W
    
    rectW = list( np.random.randint(0, W, 2) )
    rectL = list( np.random.randint(0, L, 2) )
    #picks two values per dimension, determines range of length & width
    rectW.sort()
    rectL.sort()
    #sort coordinates in an increasing order
    
    rectRange = tuple( rectL + rectW )
    #Combine coords in pattern of (row1, row2, col1, col2)
    assert bool(len(rectRange) == 4) #Checking shape of output
    
    rectPlot = plotArray * 0 #new zeros array; gets reactangle of one's
    
    iterPlot = np.nditer( \
               rectPlot, flags=['multi_index'], op_flags=['writeonly'])
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
    assert bool( 0 < np.sum(rectPlot) == \
           (rectRange[1]-rectRange[0] +1) \
           * (rectRange[3]-rectRange[2] +1) )
    #check that the correct, non-zero area of coverage has been plotted
    return rectPlot


def remove_overlap(towerPlot, totalPlot):
    '''
    Locate where a new tower range overlaps with pre-existing coverage.
    
    :@param towerPlot: numpy array, coverage for a random tower
    :@param totalPlot: numpy array, pre-existing coverage in a plot
    :@return: numpy array, new area covered by tower
    '''
    import numpy as np
    
    assert isinstance(towerPlot, np.ndarray), \
           "Tower input not a numpy array"
    assert isinstance(totalPlot, np.ndarray), \
           "Pre-existing plot input not a numpy array"
    assert bool(towerPlot.shape == totalPlot.shape), \
           "Inputs must be the same dimensions"
    for coord in np.nditer(towerPlot):#loop thorugh each element
        assert bool(coord == 0 or coord == 1), \
               "Tower input array may only contain 0s or 1s"
    for coord in np.nditer(totalPlot): #loop thorugh each element
        assert bool(coord == 0 or coord == 1), \
               "Tower input array may only contain 0s or 1s"
    
    if np.array_equal(totalPlot, np.zeros( totalPlot.shape )):
        #compares input to same-dimension array of zeros
        return towerPlot
        #If there is no coverage already, just return the new coverage
    else:
        pass
    
    layerPlot = (towerPlot * 2) + totalPlot
    #Layers the two plots together
    #new coverage = 2, old coverage = 1, no coverage = 0, overlap = 3
    
    iterPlot = np.nditer( layerPlot, op_flags=['writeonly'] )
    #lets the function iterate element-wise over the layer and rewrite
    while not iterPlot.finished:
        if iterPlot[0] == 2: #looks for new coverage
            iterPlot[0] = 1 #new coverage is now 1
        else:
            iterPlot[0] = 0 #all pre-existing coverage becomes 0
        iterPlot.iternext() #points to next element
    
    assert bool( np.sum(layerPlot) <= np.sum(towerPlot) )
    #check that the layer does not exceed the size of the tower coverage
    assert bool( layerPlot.shape == totalPlot.shape)
    #check that the dimensions haven't changed
    return layerPlot


def trim_coverage(coverPlot):
    '''
    From a plot of signal coverage, find the largest rectangular range
    within that coverage.
    
    :@param coverPlot: numpy array, 1 represents coverage; 0 is none
    :@return: numpy array, largest rectangle inside of coverPlot
    '''
    import numpy as np
    
    assert isinstance(coverPlot, np.ndarray), \
           "New coverage input must be a numpy array"
    for coord in np.nditer(coverPlot):#loop thorugh each element
        assert bool(coord == 0 or coord == 1), \
               "Coverage input array may only contain 0s or 1s"
    
    def collect_slices(plotSlice):
        '''
        Takes in a slice from the coverage plot and identifies where in
        that slice there is coverage
        
        :@param plotSlice: numpy array, a 1-D slice from coverage plot
        :@return: list of tuples describing where there is coverage
        '''
        prevElement = 0 #tracks value of element in previous index
        foundRanges = [] #stores tuples for elements found
        start = 0 #start coordinate of a coverage range
        
        for i in range( len(plotSlice) ): #loop over the slice
            if plotSlice[i] == 1 and prevElement == 0:
            #When it first runs into a 1 / enters range of coverage
                start = i #set the start coordinate
            elif plotSlice[i] == 0 and prevElement == 1:
            #When it exits a range of coverage (first encounters a 0)
                foundRanges.append((start, i - 1))
                #adds the range found to the list of ranges
            else:
                pass #do nothing if not at a coverage boundary
            
            if plotSlice[i] == 1 and i == len(plotSlice) -1:
            #if it reaches the end of the array on a 1
                foundRanges.append((start, i))
                #append to the list since there is no next value
            else:
                pass
            prevElement = plotSlice[i] #store this for the next loop
        
        return foundRanges #give back the tuples describing the ranges
    
    
    

class rectangle:
    '''
    An object which describes a rectangle by the upper and lower bounds
    of its vertical and horizontal dimensions, inclusive.
    
    A way to intuitively manipulate rectangles to make the
    trimming by largest area process easier to handle.
    '''
    
    def __init__(self, firstRow, lastRow, leftCol, rightCol):
    #r for rows; c for columns; 1 for lower and 2 for upper bounds
        assert bool(firstRow <= lastRow), \
               "Row locations should be in increasing order"
        assert bool(leftCol <= rightCol), \
               "Column locations should be in increasing order"
        self.r1 = firstRow
        self.r2 = lastRow
        self.c1 = leftCol
        self.c2 = rightCol
        self.lrange = (firstRow, lastRow)
        self.wrange = (leftCol, rightCol)
        self.length = lastRow - firstRow + 1
        self.width = rightCol - leftCol + 1
    
    def __add__(rect1, rect2):