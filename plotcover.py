'''
Displays arrays in a graphical format for easier visualization.
'''

def plot_oneArray(inArray):
    '''
    Plots a single array representing coverage on an xy axes.
    '''
    import matplotlib.pyplot as plt
    import numpy as np

    plt.subplot(111)
    plt.imshow(inArray, aspect='equal')
    
    plt.show()
    plt.close()

    
def plot_towersToFill(resultList):
    '''
    Makes a histogram of the results from sample_towersToFill.
    X-axis is the number of towers required to fill and the y-axis is
    the number of instances for each result.
    '''
    import matplotlib.pyplot as plt
    import numpy as np
    
    plt.hist(resultList)
    plt.show()
    plt.close()