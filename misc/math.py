import numpy as np
from misc.buffer import Buffer

def slope_of(data):
    """
    #The slope between two points is given by the following formula
    #Points (x1, x2), (y1, y2)
    #Slope = (y2 - y1)/(x2-x1)
    """
    slope = [0] * len(data)
    i = 0
    for x1 in data:
        if i + 1 < len(data):
            slope[i] = (data[i + 1] - x1) / 1
        i = i + 1
    return slope[:-1]

def slope_steps(data,step):
    """
    #The slope between two points is given by the following formula
    #Points (x1, x2), (y1, y2)
    #Slope = (y2 - y1)/(x2-x1)
    """
    slope = []
    i = 0
    buffer = Buffer(step)
    for subset in data:
        buffer.add(subset)
        if buffer.isFull():
            for x1 in buffer.data:
                if i + 1 < len(data):
                    #print(buffer.data)
                    slope.append((data[i + 1] - x1) / 1)
                i = i + 1
            buffer.flush()
    return slope[:-1]
