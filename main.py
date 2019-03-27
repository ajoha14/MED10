import argparse
import numpy as np
from numpy.distutils.system_info import f2py_info

from Signals.ArduinoSerialPortCommunicator import SerialReader
from misc.logging import Logger
import misc.logging as logging
from misc.buffer import Buffer
import misc.math as math
import matplotlib.pyplot as plt
import keyboard

#Initialization - Arguments
parser = argparse.ArgumentParser(description="Multi Modal Affect Detection")
parser.add_argument("-debug", default=False, action="store_true", help="Enables debug mode")
args = parser.parse_args()


#Testing Area
def testing():
    print("testing")
#Testing Area

def __main__():
    if args.debug:
        print("RUNNING IN DEBUG MODE")
    worker = Worker()
    worker.work()

class Worker:
    looping = True

    def __init__(self):
        self.serialport = SerialReader(port='COM5')

    def work(self):
        keyboard.add_hotkey('space', self.toogleLoop, args=())
        if self.serialport.ser is not None:
            log = Logger()
            gsrbuffer = Buffer(10000)
            while self.looping:
                currentData = self.serialport.current_data()
                if currentData is not 'error':
                    log.logString(currentData)
                """    time, gsr, hr = currentData.split(',', 3)
                    gsr, hr = int(gsr), int(hr)
                    gsrbuffer.add(gsr)
                    #print(gsrbuffer.data)
                if gsrbuffer.isFull():
                    break
                    #print(sum(math.slope_of(gsrbuffer.data)))"""
        else:
            print("Arduino not plugged in. Loading data from log instead")
            gsrList = logging.getGSRFromLog("Logs/onlyGSR.csv")
            print(gsrList)
            mean = math.moving_average(gsrList,100)
            #slope =math.slope_of(gsrList)
            #subslope = math.slope_steps(gsrList,30)
            #print(slope)
            #print(subslope)
            #print(sum(subslope))
            #print(sum(slope))
            #print(np.mean(slope))
            #print(np.mean(subslope))
            plt.figure(1)
            plt.plot(gsrList)
            plt.figure(2)
            #plt.plot(slope)
            #plt.plot(subslope)
            plt.plot(mean)
            plt.show()

    def toogleLoop(self):
        print("Toogling Loop...")
        self.looping = not self.looping


__main__()


