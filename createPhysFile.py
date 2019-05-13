from Signals.hrProc import hrProcesser
from misc.buffer import Buffer
import misc.QuickMaths as qm
import os
import matplotlib.pyplot as plt
import numpy as np
import cv2

path = "Logs/Water/P1/"

for file in os.listdir(path):
    with open(path + file) as f:
        logData = np.array(f.read().splitlines())

        data_out = open("logWithHr.csv","w")
        hrData = []
        hrsData = []
        tsData = []
        gsrData = []
        indexes = []

        HRp = hrProcesser()
        hrbuffer = Buffer(size=100)
        gsrbuffer = Buffer(size=100)
        tsbuffer = Buffer(size=100)

        for i in range(1,len(logData)):
            #split log data
            log_data = logData[i].split(',')
            if len(log_data) >= 3:
                #make buffers
                tsbuffer.add(log_data[0])
                gsrbuffer.add(float(log_data[1]))
                hrbuffer.add(float(log_data[2]))

                #TIMESTAMP,HR,HRV,GSR
                if len(hrbuffer.data) == hrbuffer.size:
                    #Do calculations
                    hrdat = np.asarray(qm.moving_average(hrbuffer.data,window=10))
                    tsdat = np.asarray(tsbuffer.data)
                    l = qm.ampd(hrdat,limit=0.5) #Peak Detectoin
                    hrs = HRp.HR(hrdat,tsdat)
                    hrData.append(float(log_data[2]))
                    hrsData.append(hrs)
                    gsrData.append(float(log_data[1]))
                    data_out.write("{},{},{}".format(log_data[0], hrs, float(log_data[1])))

                    tsData.append(log_data[0])
            else:
                indexes.append(i)

        plt.plot(hrData)
        plt.plot(hrsData)
        for index in indexes:
            plt.axvline(index,color="r")
        plt.plot(gsrData)
        plt.show()