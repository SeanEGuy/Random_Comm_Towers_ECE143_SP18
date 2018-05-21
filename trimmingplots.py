'''
A module exclusively for trimming down the non-overlapping area of a
2-dimensional area into the largest rectangle possible.

This is just a separate dummy file where I am attempting a different
strat to trimming than what is being coded (as of 5PM, 5/20/18, PST)
is the main module, commtower.py.

Old method:
1.  Collect horizontal and vertical slices from a plot.
2.  Find where in each slice there is coverage (1s in the array)
3.  Compare slices. If adjacent slices have the same ranges, combine
    ranges to generate the rectangle.
4.  Compare rectangle areas.
Pros: Generates relatively few rectangles. Lighter on memory.
Cons: Combining slices and keeping track of locations is difficult.


New Method:
1.  Iterate through each element in the coverage array.
2.  Once coverage is found, make two rectangles from that point.
    One rectangle goes as far right as it can and then sweeps down.
    The other goes as far down as it can then sweeps right.
3.  Generate a rectangle pair for every coverage point in the plot.
4.  Compare rectangles.
Pros: Much easier to manage if just a few if statements. No having to
      recombine random bits of data.
Cons: Makes a lot of rectangles.
'''

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
    
    def sweep_from_corner(inPlot, r1, c1,transposed=False):
        '''
        Given a starting point, generate one rectangle sweeping right
        then down and another sweeping down then right until they reach
        the boundary of coverage.
        
        :@param inPlot: ndarray, original non-overlapping coverage
        :@param r1: int, row index to start from
        :@param c1: int, col index to start from
        :@param transposed: bool, whether the input was transposed
        '''
        
        length, width = inPlot.shape #dimensions as easy to read vars
        c2 = c1 #last column is called; can increase from here
        r2 = r1 #last row is called; can increase from here
        
        for i in range(c1, width):
        #loop through column c1 to the right
            if inPlot[r1][i] == 1 and i > width - 1:
                pass #keep going until zero or end is reached
            else:
                c2 = i #assign column 2 as last column
                break #done once c2 is assigned
        
        for j in range(r1, length):
        #loop thorugh each row
            if 0 in inPlot[j][c1:c2]:
            #check for zeros in each row; the first should never fail
                c2 = j - 1 #save the index of last successful row
                break
            elif j == length - 1:
                c2 = j #just save last row if it goes to the end
            else: #Do nothing for other 1 locations
                pass
        
        outPlot = inPlot * 0 #new plot to add the new rectangle
        iterOut = np.nditer(outPlot, \
                  flags=['multi_index'], op_flags=['writeonly'])
        #iterate over each element and apply 1s in rectange range
        while not iterOut.finished:
            i,j = iterOut.index
            if r1 <= i <= r2 and c1 <= j <= c2:
            #check if indices in range of r1-r2 & c1-c2
                iterOut[0] == 1 #change to 1 if in coverage
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
            i,j = itPlot.index
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
    randRect = largestRect[ np.random.randint(0,len(allLargest)) ]
    #pick a random rectangle from the list to limit bias
    
    assert bool(randRect.shape == inPlot.shape)
    #end result should still be the same dimensions as the start
    return randRect