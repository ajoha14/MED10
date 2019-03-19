import numpy as np
from datetime import datetime
from misc.buffer import Buffer

class hrProcesser:
    def __init__(self, bd, sl):
        self.ptf = 'C:/Users/Anders S. Johansen/Desktop/data.txt'
        self.baud = bd
        self.sampleLength = sl
        self.hrbuffer = Buffer(self.sampleLength * self.baud)
    
    def peakDetection(self, data):
        peaks = []

        return peaks

    def heartRate(self, data):
        tt = 0
        for i in range(len(data)-1):
            d1 = datetime.strptime(data[i],'%m%d-%H%M_%S.%f')
            d2 = datetime.strptime(data[i+1],'%m%d-%H%M_%S.%f')
            tt += d2-d1
        hr = tt / d
        
