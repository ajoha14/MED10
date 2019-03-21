from Signals.hrProc import hrProcesser
from misc.buffer import Buffer
import matplotlib.pyplot as plt
import numpy as np

c = hrProcesser()
buffer = Buffer()
with open("C:/Users/Anders S. Johansen/Desktop/data2.txt") as f:
    d = f.read().splitlines()

#SETUP LIVE PLOTTER
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(1,1,1)

for i in range(len(d)):
    a = np.array(d[i].split(','))
    buffer.add(a)
    print(buffer.data[0][1])
    if len(buffer.data) == buffer.size:
        
        #Do calculations
        l = c.ampd(buffer.data[0][:]) #Peak Detectoin
        
        #Update plot
        ax.clear()
        ax.plot(buffer.data[:][0])
        ax.scatter(l,buffer.data[l][0])
        plt.show()
        plt.pause(0.001)

