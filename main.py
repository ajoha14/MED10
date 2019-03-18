import argparse
from Signals.ArduinoSerialPortCommunicator import SerialReader
from misc import logger
from datetime import datetime

#Initialization - Arguments
parser = argparse.ArgumentParser(description="Multi Modal Affect Detection")
parser.add_argument("-debug", default=False, action="store_true", help="Enables debug mode")
args = parser.parse_args()

#Initialization - Sawyer

#Initialization - Arduino


def __main__():
    if args.debug:
        print("RUNNING IN DEBUG MODE")
    serialport = SerialReader('COM5')
    logger.create_new_log()
    while True:
        logger.log_custom(serialport.current_data())

__main__()


