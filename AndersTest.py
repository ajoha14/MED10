from Signals.hrProc import hrProcesser
from misc.buffer import Buffer
import matplotlib.pyplot as plt
import numpy as np

c = hrProcesser()
hrbuffer = Buffer(size=500)
tsbuffer = Buffer(size=500)
with open("Logs/AndersTestLog.csv") as f:
    data = np.array(f.read().splitlines())


#SETUP LIVE PLOTTER
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(1,1,1)


for i in range(len(data)):
    hrbuffer.add(float(data[i].split(',',3)[2]))
    tsbuffer.add(data[i].split(',',3)[1])
    if len(hrbuffer.data) == hrbuffer.size:       
        print(hrbuffer.data)
        print(tsbuffer.data)
        #Do calculations
        l = c.ampd(hrbuffer.data) #Peak Detectoin  
        hrs = c.heartRate(hrbuffer.data,tsbuffer.data)   
        #Update plot
        ax.clear()
        ax.set_title("HearRate: {}".format(hrs))
        ax.plot(data)
        ax.scatter(l,data[l])
        plt.show()
        plt.pause(0.001)

