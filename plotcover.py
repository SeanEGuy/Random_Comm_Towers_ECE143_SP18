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