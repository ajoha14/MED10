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
            slope[i] = (data[i + 1] - x1)
        i = i + 1
    return slope[:-1]

def slope_steps(data,step):
    """
    #The slope between two points is given by the following formula
    #Points (x1, x2), (y1, y2)
    #Slope = (y2 - y1)/(x2-x1)
    """
    slope = []
    buffer = Buffer(step)
    for subset in data:
        buffer.add(subset)
        if buffer.isFull():
            subslope = slope_of(buffer.data)
            mean = np.mean(subslope)
            slope.append(mean)
            buffer.flush()
    return slope

def moving_average(signal, window):
        smoothedSignal = []
        for i in range(window, len(signal)):
            smoothedSignal.append(np.mean(signal[i-window:i]))
        return np.asarray(smoothedSignal)

def ampd(sigInput, limit = 1): #by https://github.com/LucaCerina/ampdLib          
        #Create preprocessing linear fit	
        sigIn = np.arange(0, len(sigInput))
        
        #Calculate detrending
        dtrSignal = (sigInput - np.polyval(np.polyfit(sigIn, sigInput, 1), sigIn)).astype(float)
        N = len(dtrSignal)
        L = int(np.ceil(N*limit / 2.0)) - 1
        
        #Generate matrix of Ones
        LSM = np.ones([L,N], dtype='uint8')
        
        #Local minima extraction
        for k in range(1, L):
            LSM[k - 1, np.where((dtrSignal[k:N - k - 1] > dtrSignal[0: N - 2 * k - 1]) & (dtrSignal[k:N - k - 1] > dtrSignal[2 * k: N - 1]))[0]+k] = 0
        
        #Isolate Peaks
        pks = np.where(np.sum(LSM[0:np.argmin(np.sum(LSM, 1)), :], 0)==0)[0]
        return pks