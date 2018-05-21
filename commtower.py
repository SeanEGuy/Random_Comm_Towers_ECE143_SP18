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


def get_largest_rectangle(inPlot):
    '''
    Makes candidate rectangles inside of the input plot where coverage
    is indicated. Finds and returns the largest one. Note that the
    coverage has already been trimmed for overlap with pre-existing
    towers.
    
    :@param inPlot: ndarray, original non-overlapping coverage
    :@return: ndarray, larest rectangular coverage from inPlot
    '''
    import numpy as np
    
    #asserts go here
    
    rectList = [] #store tuples representing rectangles
    
    def sweep_from_corner(thePlot, r1, c1,transposed=False):
        '''
        Given a starting point, generate one rectangle sweeping right
        then down and another sweeping down then right until they reach
        the boundary of coverage.
        
        :@param inPlot: ndarray, original non-overlapping coverage
        :@param r1: int, row index to start from
        :@param c1: int, col index to start from
        :@param transposed: bool, whether the input was transposed
        '''
        
        length, width = thePlot.shape #dimensions as easy to read vars
        c2 = c1 #last column is called; can increase from here
        r2 = r1 #last row is called; can increase from here
        
        for i in range(c1, width):
        #loop through column c1 to the right
            if thePlot[r1][i] == 1:
                c2 = i #assign column 2 as last successful column
            else:
                break #done once c2 is assigned
        
        for j in range(r1, length):
        #loop thorugh each row
            if 0 not in thePlot[j][c1:c2+1]:
            #check for zeros in each row; the first should never fail
                r2 = j #save the index of last successful row
            else: #Do nothing for rows with 1
                break
        
        outPlot = thePlot * 0 #new plot to add the new rectangle
        iterOut = np.nditer(outPlot, \
                  flags=['multi_index'], op_flags=['writeonly'])
        #iterate over each element and apply 1s in rectange range
        while not iterOut.finished:
            k,l = iterOut.multi_index
            if r1 <= k <= r2 and c1 <= l <= c2:
            #check if indices in range of r1-r2 & c1-c2
                iterOut[0] = 1 #change to 1 if in coverage
            else:
                pass
            iterOut.iternext()
        
        if transposed == True:
            return np.transpose(outPlot)
        else:
            return outPlot
    
    itPlot = np.nditer(inPlot, flags=['multi_index'])
    #make an iterable for inPlot with indices available
    while not itPlot.finished:
        if itPlot[0] == 1:
            i,j = itPlot.multi_index
            rectList.append( sweep_from_corner(inPlot, i, j) )
            #making largest rectangle by going right then down
            rectList.append( \
            sweep_from_corner(np.transpose(inPlot), j, i, True) )
            #biggest rectangle sweeping down the right
            #done by transposing the array at the start and end
        itPlot.iternext()
    
    #rectList should now have all the largest rectangles in coverage
    largestRect = max(rectList, key=lambda rarray: np.sum(rarray))
    #finding the largest rectangles by taking the sum of each array
    assert bool(np.sum(largestRect) <= np.sum(inPlot))
    #largest trim shouldn't be greater than the original coverage
    
    allLargest = [largestRect]
    #listing all of the largest rectangles in case of ties
    for bigRect in rectList:
        if np.sum(bigRect) == np.sum(largestRect):
        #compare coverage areas
            allLargest.append(bigRect) #list it if it's just as big
        else:
            pass
    randRect = allLargest[ np.random.randint(0,len(allLargest)) ]
    #pick a random rectangle from the list to limit bias
    
    assert bool(randRect.shape == inPlot.shape), "%s" % (randRect)
    #end result should still be the same dimensions as the start
    return randRect