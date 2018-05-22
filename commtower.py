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
    :@return: ndrray, int, zeros representing no coverage
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
    given plot of land. Does not deal with overlapping and trimming.
    
    Numpy module must be available. Asserts that the input is a
    two-dimensional numpy array after importing numpy.
    
    Grabs the dimensions of the array and stores in L and w. Using
    randint, two indices per dimensions are chosen. These are sorted and
    combined in a tuple that describes the ranges, inclusive, in which
    the final rectangle will be.
    
    An array of the same dimensions as the input is generated. It is
    made iterable by np.nditer(). By iterating element-wise and
    comparing each element's row and column indices to the rectangle
    ranges, the function finds the nodes that should be ones and
    leaves the remainder as zeros.
    
    The output array is checked for correct dimensions and whether it
    only contains zeros and ones. It is then returned as the output.
    
    :@param plotArray: ndarray, dimensions represent a plot of land
    :@return: ndarray, plot with random coverage rectangle mapped out
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
    Imports numpy and asserts that inputs are numpy arrays of the same
    dimensions. It then checks whether only zeros or ones are in the
    arrays.
    
    Numpy module must be available to function.
    
    If totalPlot, the pre-existing coverage, only has zeros, the tower
    plot is simply returned. Otherwise, the function continues to
    combining both input plots. The tower plot is multiplied by 2 and
    added to the pre-existing coverage. Thus, values of 2 in the
    new layerPlot indicate coverage from the tower that does not
    overlap with the pre-existing coverage.
    
    To generate the output, the function iterates element-wise over the
    layerPlot and replaces 2's with one and everything else with zero.
    This output is checked such that its dimensions are the same as the
    inputs and its coverage does not exceed that of the tower input.
    
    :@param towerPlot: ndarray, coverage for a random tower
    :@param totalPlot: ndarray, pre-existing coverage in a plot
    :@return: ndarray, new area covered by tower
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
    
    Module numpy must be available to function.
    
    First import numpy and check that the input plot is a numpy array
    containing only ones or zeros. Second define a method to create
    rectangles starting from a single point and extending out to the
    limits of coverage.
    
    Looping through each element in the input plot, each one is checked
    for being either zero or one. Zero values are ignored. Ones have
    their row and column indices fed into the encapsulated function
    along with the input plot, yielding a plot with rectangular coverage
    that is stored in a holding list. The function is called again on
    transposition of the input and indices to yield another rectangle
    from that corener.
    
    If the list of rectangles ends up empty, an empty array is returned
    as the final output. Otherwise, the rectangle with the maximum array
    sum is identified using a lambda argument insied of max().
    
    To find rectangles that may have the same area, the rectangle
    candidate list is looped over, this time comparing each item's
    sum to the one picked out. If multiple plots have the same area,
    one is chosen randomly by generating a random integer index from
    a uniform distribution.
    
    This output is checked so that its dimensions match the output and
    that its locations of ones is a subset of the input file's
    locations. This array of the trimmed, rectangular coverage is
    finally returned as the output.
    
    :@param inPlot: ndarray, original non-overlapping coverage
    :@return: ndarray, largest rectangular coverage from inPlot
    '''
    import numpy as np
    
    assert isinstance(inPlot, np.ndarray), \
           "Input must be a numpy array"
    for coord in np.nditer(totalPlot): #loop thorugh each element
        assert bool(coord == 0 or coord == 1), \
               "Input array may only contain 0s or 1s"
    
    def sweep_from_corner(thePlot, r1, c1,transposed=False):
        '''
        Given a starting point, generate one rectangle sweeping right
        then down and another sweeping down then right until they reach
        the boundary of coverage.
        
        The inputs designate the upper-left corner of the rectangular
        coverage. Plot dimensions are saved from thePlot (same as
        inPlot from the outer function). Ending row and column are
        initially the same as the starting ones.
        
        The function loops through columns indices, checking which
        elements on the same row also contain ones and thus are part of
        the coverage. Then the function sweeps down, checking its slice
        of row for zero values. The last indices are saved as the last
        row and column.
        
        A new plot is created. It is populated by zeros and ones by
        iterating over each element and checking whether its indices
        fall within the deteermined coverage rectangle. Coverage means
        one and no coverage is zero.
        
        If transposed is true, the function transposes result before
        returning it as a result. Otherwise the function simply returns
        in its current state.
        
        :@param inPlot: ndarray, original non-overlapping coverage
        :@param r1: int, row index to start from
        :@param c1: int, col index to start from
        :@param transposed: bool, whether the input was transposed
        :@return: ndarray, plotted largest rectangle from r1,c1
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
            else: #Stop when reaches a row with 0
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
        
        assert outPlot.shape == thePlot.shape
        #should generate a plot with the same shape as input
        assert np.sum(outPlot) =< np.sum(thePlot)
        #total coverage of output can't be more than input
        
        if transposed == True: #if input transposed before
            return np.transpose(outPlot)
            #transpose plot to return to original orientation
        else:
            return outPlot #return detected subset of coverage
    
    rectList = [] #store arrays representing rectangles of coverage
    
    itPlot = np.nditer(inPlot, flags=['multi_index'])
    #make an iterable for inPlot with indices available
    while not itPlot.finished:
        if itPlot[0] == 1:
        #finds each location in coverage from input
            i,j = itPlot.multi_index
            rectList.append( sweep_from_corner(inPlot, i, j) )
            #making largest rectangle by going right then down
            rectList.append( \
            sweep_from_corner(np.transpose(inPlot), j, i, True) )
            #biggest rectangle sweeping down the right
            #done by transposing the array at the start and end
        itPlot.iternext()
    
    #rectList should now have all the largest rectangles in coverage
    if len(rectList) == 0:
        assert np.sum(inPlot) == 0, "No rectangle found:\n%s\n" % inPlot
        #Gets empty list if input is only an array of zeros
        return inPlot * 0
        #returns an array of zeros if no rectangles found
    else:
        pass #keep going if there are rectangles
    
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
    assert (-1) not in (inPlot - randRect)
    #ensures that newly trimmed coverage is within the original
    return randRect


    
def plot_ntowers(L, W, n=0):
    '''
    Tracks coverage as towers are randmly placed in a designated plot of
    land. Can calculate the coverage from n towers or count the number
    of towers required to fill the plot completely.
    
    Numpy module must be available to function.
    
    Dimensions are checked to be postive integers. Same for n, except it
    may equal zero.
    
    It then creates an empty plot to be filled with towers. The loop
    goes through making a tower, removing its overlap with other
    coverages, trimming back into a rectangle, adding the coverage
    into the main plot, and tracking the number of towers built.
    
    The loop ends if the plot is completely covered or if input n is
    non-zero and that many towers have been built.
    
    Asserts that the number of towers counted is a positive integer
    value. Also checks that the proportion of the total plot covered
    is greater than zero and less than or equal to one.
    
    n is zero, then the number of towers used to fill the plot is
    returned as the output. Otherwise, the area covered--found by
    taking the sum of the main plot array--and the proportion of total
    area covered is returned inside a two-element tuple.
    
    :@param plotLen: int, length of the plot; stored as rows in an array
    :@param plotWidth: int, width of plot; stored as columns in an array
    :@param n: int, towers built; if 0, will count towers to fill.
    :@return: tuple, total area and proportion covered
              OR
              int, towers built to fill plot if n=0
    '''
    import numpy as np
    
    assert isinstance(L, int) and L > 0, \
           "Length must be a positive integer."
    assert isinstance(W, int) and W > 0, \
           "Width must be a positive integer."
    assert isinstance(n, int) and n >= 0, \
           "n must be an integer and > or = 0"
    
    mainPlot = plot_land(L,W) #generate the empty plot
    totalArea = L * W
    
    nBuilt = 0 #tracks number of towers built; says when to exit loop
    finished = 0 
    while finished == 0: #may be changed by different events to end loop
        randTower = make_random_tower(mainPlot)
        #generate a tower with random rectangular coverage
        overlapFree = remove_overlap(randTower, mainPlot)
        #remove parts of coverage already in the main plot
        trimTower = get_largest_rectangle(overlapFree)
        #find the largest rectangle in the remaining region
        mainPlot += trimTower
        #add the new coverage to the rest of the coverage
        nBuilt += 1 #counting towers
        if nBuilt == n and n != 0 \
           or np.sum(mainPlot) == totalArea:
        #checking whether its reached n-towers or filled the whole plot
            finished += 1
        else:
            pass
    
    assert isinstance(nBuilt, int) and nBuilt > 0
    #The number of towers must be an integer 1 or greater
    ratioCovered = np.sum(mainPlot) / float(totalArea)
    assert 0 < ratioCovered <= 1
    #The proportion of the area covered is between 0 and 1
    
    
    if n == 0: #no number of towers given
        return nBuilt #return n towers built
    else:
        return ( np.sum(mainPlot), round(ratioCovered, 3) )
        #return tuple, number of 1s in the plot and
        #the proportion of the area they cover (decimal).



def sample_towersToFill(L, W, n=100):
    '''
    To estimate the number of towers needed to fill a plot of land, this
    function simulates the process of filling a plot up for n
    repetitions.
    
    Asserts that all inputs are positive integers, then runs a loop for
    n iterations collecting the number of towers used each time a plot
    is filled. These results are stored as a list of integers.
    
    Before returning the results in a list, the list is checked for
    appropriate length n and content (integers only).
    
    :@param L: int, length dimension of the plot
    :@param W: int, width dimension of the plot
    :@return: dict, results with the number of times they occurred
    '''
    
    for funVars in [L, W, n]:
        assert isinstance(funVars, int) and bool(funVars > 0), \
            "%s must be a positive integer." % (funVars)
        #All inputs must be positve integers
    
    resultList = [] #List of tower counts from filling the plot
    for i in range(n):
        resultList.append( plot_ntowers(L, W, 0) )
        #append the result of filling the plot
    
    assert len(resultList) == n
    #check that the right number of iterations was made
    for result in resultList:
        assert isinstance(result, int) and result > 0
        #number of towers should be postive integer
    
    return resultList
        