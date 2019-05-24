from Signals.hrProc import hrProcesser
from misc.buffer import Buffer
import misc.QuickMaths as qm
import os
import matplotlib.pyplot as plt
import numpy as np
import cv2

path = "Logs/Water/P13/"

for file in os.listdir(path):
    with open(path + file) as f:
        print("opening file: ", file)
        logData = np.array(f.read().splitlines())

        data_out = open("logWithHr.csv","w")
        hrData = []
        hrsData = []
        tsData = []
        gsrData = []
        indexes = []
        markers = []
        offset = 150

        HRp = hrProcesser()
        buffersize = 100
        hrbuffer = Buffer(size=buffersize)
        gsrbuffer = Buffer(size=buffersize)
        tsbuffer = Buffer(size=buffersize)

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
                    hrsData.append(hrs)
                    data_out.write("{},{},{}".format(log_data[0], hrs, float(log_data[1])))
                    tsData.append(log_data[0])
                else:
                    hrsData.append(0)
                gsrData.append(float(log_data[1]))
                hrData.append(float(log_data[2]))

            if len(log_data) == 1 and log_data is not "":
                indexes.append(i)
            if len(log_data) == 2:
                markers.append(i)
        gsrmin = min(gsrData)
        gsrData = [x + offset - gsrmin for x in gsrData]

        for k in range(0,len(hrsData)):
            if hrsData[k] > 200: hrsData[k] = 0


        #plt.plot(hrData)
        plt.plot(hrsData)
        for index in indexes:
            plt.axvline(index,color="r")
        for index in markers:
            plt.axvline(index, color="brown")
        plt.plot(gsrData)
        plt.title(file)
        plt.show()