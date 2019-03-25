import numpy as np
import datetime
from misc.buffer import Buffer

class hrProcesser:
    def __init__(self):
        self.dtFormat = '%m_%d-%H_%M_%S.%f'

    def heartRate(self, hrSig, hrTimestamp, minPeaks=3):
        peaks = self.ampd(hrSig)
        if len(peaks) > minPeaks:
            peaksTimeStamps = hrTimestamp[peaks]
            totalTime = datetime.timedelta(microseconds=0)
            for i in range(len(peaksTimeStamps)-1):
                d1 = datetime.datetime.strptime(peaksTimeStamps[i], self.dtFormat)
                d2 = datetime.datetime.strptime(peaksTimeStamps[i+1], self.dtFormat)
                totalTime += d2 - d1
            return ((len(peaksTimeStamps)-1) / totalTime.total_seconds()) * 60
        else:
            return 0.0

    def smoothSignal(self, signal, window=10):
        smoothedSignal = []
        for i in range(len(signal)-window):
            smoothedSignal.append(np.mean(signal[i:i+window]))
        return np.asarray(smoothedSignal)


    def ampd(self, sigInput, limit = 1): #by https://github.com/LucaCerina/ampdLib          
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