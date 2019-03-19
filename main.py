import argparse
import numpy as np
from numpy.distutils.system_info import f2py_info

from Signals.ArduinoSerialPortCommunicator import SerialReader
from misc.log import Logger
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
        self.serialport = SerialReader('COM5')

    def work(self):
        log = Logger()
        keyboard.add_hotkey('space', self.toogleLoop, args=())

        while self.looping:
            log.logString(self.serialport.current_data())

        print(log.currentSessionName)
        print(log.getDataFromLog(log.currentSessionName))
        # math.slope_of()

    def toogleLoop(self):
        self.looping = not self.looping


__main__()


