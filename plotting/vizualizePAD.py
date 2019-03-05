from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np


##### Initialization #####
fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')
#Label axis
ax.set_xlabel('Pleasure')
ax.set_ylabel('Arousal')
ax.set_zlabel('Dominance')
#Set axis limits
ax.set_xlim3d(-1,1)
ax.set_ylim3d(-1,1)
ax.set_zlim3d(-1,1)
#set ticks
ax.set_xticks([-1, -0.5, 0, 0.5, 1])
ax.set_yticks([-1, -0.5, 0, 0.5, 1])
ax.set_zticks([-1, -0.5, 0, 0.5, 1])

#Show Current State
state = [0,0,0] #Order; Pleasure, Arousal, Dominance

#Visualize Mental State
while(True):
    ax.scatter(state[0], state[1], state[2], c='r', marker='o')
    plt.show()
    plt.pause(0.05)