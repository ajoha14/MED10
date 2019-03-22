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

    def ampd(self, sigInput, LSMlimit = 1): #by https://github.com/LucaCerina/ampdLib
        """Find the peaks in the signal with the AMPD algorithm.
            Original implementation by Felix Scholkmann et al. in
            "An Efficient Algorithm for Automatic Peak Detection in 
            Noisy Periodic and Quasi-Periodic Signals", Algorithms 2012,
            5, 588-603
            Parameters
            ----------
            sigInput: ndarray
                The 1D signal given as input to the algorithm
            lsmLimit: float
                Wavelet transform limit as a ratio of full signal length.
                Valid values: 0-1, the LSM array will no longer be calculated after this point
                which results in the inability to find peaks at a scale larger than this factor.
                For example a value of .5 will be unable to find peaks that are of period 
                1/2 * signal length, a default value of 1 will search all LSM sizes.
            Returns
            -------
            pks: ndarray
                The ordered array of peaks found in sigInput
        """            
        # Create preprocessing linear fit	
        sigTime = np.arange(0, len(sigInput))
        
        # Detrend
        dtrSignal = (sigInput - np.polyval(np.polyfit(sigTime, sigInput, 1), sigTime)).astype(float)
        
        N = len(dtrSignal)
        L = int(np.ceil(N*LSMlimit / 2.0)) - 1
        
        # Generate random matrix
        LSM = np.ones([L,N], dtype='uint8')
        
        # Local minima extraction
        for k in range(1, L):
            LSM[k - 1, np.where((dtrSignal[k:N - k - 1] > dtrSignal[0: N - 2 * k - 1]) & (dtrSignal[k:N - k - 1] > dtrSignal[2 * k: N - 1]))[0]+k] = 0
        
        pks = np.where(np.sum(LSM[0:np.argmin(np.sum(LSM, 1)), :], 0)==0)[0]
        return pks