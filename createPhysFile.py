from Signals.hrProc import hrProcesser
from misc.buffer import Buffer
import misc.QuickMaths as qm

import matplotlib.pyplot as plt
import numpy as np
import cv2

with open("Logs/Lego/P21/05_07-09_34_23.csv") as f:
    logData = np.array(f.read().splitlines())

    data_out = open("logWithHr.csv","w")
    hrData = []
    gsrData = []

    HRp = hrProcesser()
    hrbuffer = Buffer(size=100)
    gsrbuffer = Buffer(size=100)
    tsbuffer = Buffer(size=100)

    for i in range(1,len(logData)):
        #split log data 
        log_data = logData[i].split(',',3)
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
                hrData.append(hrs)
                gsrData.append(float(log_data[1]))
                data_out.write("{},{},{}".format(log_data[0], hrs, float(log_data[1])))
    plt.plot(hrData)
    plt.plot(gsrData)
    plt.show()


    


