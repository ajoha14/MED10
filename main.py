import argparse
import numpy as np
from numpy.distutils.system_info import f2py_info

from Signals.ArduinoSerialPortCommunicator import SerialReader
from misc.logging import Logger
import misc.logging as logging
from misc.buffer import Buffer
import misc.math as math
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
                    time, gsr, hr = currentData.split(',', 3)
                    gsr, hr = int(gsr), int(hr)
                    gsrbuffer.add(gsr)
                    #print(gsrbuffer.data)
                if gsrbuffer.isFull():
                    break
                    #print(sum(math.slope_of(gsrbuffer.data)))
                log.logString(currentData)
        else:
            print("works")
            hrList = logging.getGSRFromLog("Logs/03_21-14_16_27.csv")
            print(hrList)
            print(math.slope_of(hrList))
            print(math.slope_steps(hrList,5))
            print(sum(math.slope_of(hrList)))
            print(np.mean(math.slope_of(hrList)))

    def toogleLoop(self):
        print("Toogling Loop...")
        self.looping = not self.looping


__main__()


