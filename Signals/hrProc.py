import numpy as np
import datetime
from misc.buffer import Buffer
import misc.QuickMaths as qm
import mathf

class hrProcesser:
    def __init__(self):
        self.dtFormat = '%m_%d-%H_%M_%S.%f'

    def HR(self, hrSig, hrTimestamp, minPeaks=3):
        peaks = qm.ampd(hrSig)
        if len(peaks) > minPeaks:
            peaksTimeStamps = hrTimestamp[peaks]
            totalTime = datetime.timedelta(microseconds=0)
            d1 = datetime.datetime.strptime(peaksTimeStamps[0], self.dtFormat)
            d2 = datetime.datetime.strptime(peaksTimeStamps[len(peaksTimeStamps)-1], self.dtFormat)
            totalTime += d2 - d1
            return ((len(peaksTimeStamps)-1) / totalTime.total_seconds()) * 60
        else:
            return 0.0
    
    def RMSDD(self, hrSig, hrTimestamp, minPeaks=3): #Root Mean Square of Successive Differences 
        peaks = qm.ampd(hrSig)
        RRintervals = []
        if len(peaks) > minPeaks:
            for i in range(len(peaks)-1):
                d1 = datetime.datetime.strptime(peaksTimeStamps[i], self.dtFormat)
                d2 = datetime.datetime.strptime(peaksTimeStamps[i+1], self.dtFormat)
                RR = Square((d2-d1).total_seconds())
                RRintervals.append(RR)
        return square(np.mean(RRintervals))

