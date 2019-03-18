import argparse
import numpy as np
from Signals.ArduinoSerialPortCommunicator import SerialReader
from misc import logger
import msvcrt
from misc.keyboard_listener import KeyEventThread

#Initialization - Arguments
parser = argparse.ArgumentParser(description="Multi Modal Affect Detection")
parser.add_argument("-debug", default=False, action="store_true", help="Enables debug mode")
args = parser.parse_args()

#Testing Area
def Testing():
    print("testing")
    i = 0
    step = 3
    array = [1,1,3,4,5,5,5,5,4,3,2,1,2,3,4,2,2,2,2,2,2,2,2,1,2,21,2,3,3,4,5,5,6,7,6,4,24,4,32,32,2,32]
    slope = [0] * len(array)
    for x in array:
        """
        #The slope between two points is given by the following formula
        #Points (x1, x2), (y1, y2)
        #Slope = (y2 - y1)/(x2-x1)
        """
        if i+step < len(array):
            slope[i] = (array[i+step]-x)/step
        i = i + 1
    print(array)
    slope = slope[:-step]
    print(slope)
    print(np.mean(slope))

#Testing Area


def __main__():
    if args.debug:
        print("RUNNING IN DEBUG MODE")
    serialport = SerialReader('COM5')
    logger.create_new_log()
    ket = KeyEventThread()
    ket.start()
    while True:
        logger.log_custom(serialport.current_data())
        if msvcrt.kbhit():
            break
    print(logger.currentSessionName)
    print(logger.get_data_from_log(logger.currentSessionName))
    #Testing()


__main__()


