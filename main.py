import argparse
import numpy as np
from numpy.distutils.system_info import f2py_info

from Signals.ArduinoSerialPortCommunicator import SerialReader
from misc.log import Logger
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
        #log = Logger()
        keyboard.add_hotkey('space', self.toogleLoop, args=())
        gsrbuffer = Buffer(1000)
        while self.looping:
            if self.serialport.ser is not None:
                currentData = self.serialport.current_data()
                if currentData is not 'error':
                    gsr, hr = currentData.split(',', 2)
                    gsr, hr = int(gsr), int(hr)
                    gsrbuffer.add(gsr)
                #print(gsrbuffer.data)
                if gsrbuffer.isFull():
                    print(sum(math.slope_of(gsrbuffer.data)))
                #log.logString(currentData)
            else:
                self.toogleLoop()


    def toogleLoop(self):
        self.looping = not self.looping


__main__()


