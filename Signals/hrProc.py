import numpy as np
import datetime
from misc.buffer import Buffer
import misc.math as math

class hrProcesser:
    def __init__(self):
        self.dtFormat = '%m_%d-%H_%M_%S.%f'

    def heartRate(self, hrSig, hrTimestamp, minPeaks=3):
        peaks = math.ampd(hrSig)
        if len(peaks) > minPeaks:
            peaksTimeStamps = hrTimestamp[peaks]
            totalTime = datetime.timedelta(microseconds=0)
            d1 = datetime.datetime.strptime(peaksTimeStamps[0], self.dtFormat)
            d2 = datetime.datetime.strptime(peaksTimeStamps[len(peaksTimeStamps)-1], self.dtFormat)
            totalTime += d2 - d1
            return ((len(peaksTimeStamps)-1) / totalTime.total_seconds()) * 60
        else:
            return 0.0
    
    def heartRateVariability(self):
        print('HRV not implemented yet')
        return 0
    
