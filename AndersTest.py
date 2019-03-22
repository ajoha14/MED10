from Signals.hrProc import hrProcesser
from misc.buffer import Buffer
import matplotlib.pyplot as plt
import numpy as np

c = hrProcesser()
hrbuffer = Buffer(size=500)
tsbuffer = Buffer(size=500)
with open("Logs/AndersTestLog2.txt") as f:
    data = np.array(f.read().splitlines())


#SETUP LIVE PLOTTER
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(1,1,1)


for i in range(len(data)):
    hrbuffer.add(int(data[i].split(',',3)[2]))
    tsbuffer.add(data[i].split(',',3)[0])
    if len(hrbuffer.data) == hrbuffer.size:       
        #Do calculations
        hrdat = np.asarray(hrbuffer.data)
        tsdat = np.asarray(tsbuffer.data)
        l = c.ampd(hrdat) #Peak Detectoin  
        hrs = c.heartRate(hrdat,tsdat)
        #Update plot
        ax.clear()
        ax.set_title("HeartRate: {}".format(hrs))
        plt.plot(hrbuffer.data)
        disppeaks = []
        for dp in l:
            disppeaks.append(hrbuffer.data[int(dp)])        
        plt.scatter(l,disppeaks)
        plt.show()
        plt.pause(0.001)

