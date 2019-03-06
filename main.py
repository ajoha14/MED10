import argparse
from sensors.ArduinoSerialPortCommunicator import SerialReader

#Initialization - Arguments
parser = argparse.ArgumentParser(description="Multi Modal Affect Detection")
parser.add_argument("-debug", default=False, action="store_true", help="Enables debug mode")
args = parser.parse_args()

#Initialization - Sawyer

#Initialization - Arduino


def __main__():
    if args.debug:
        print("RUNNING IN DEBUG MODE")

    serialport = SerialReader()
    while True:
        print(serialport.current_input())


__main__()


