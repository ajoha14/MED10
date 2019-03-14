import argparse
from Signals.ArduinoSerialPortCommunicator import SerialReader
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
    print("Bob")
    serialport = SerialReader('COM5')
    with open("C:/Users/Jesper W Henriksen/Dokumenter/Med10/data.txt", 'w+') as f:
        print("opened file")
        while True:
            line = str(serialport.current_input())
            print(line[2:-5])
            f.writelines(line[2:-5]+"\n")
            #+","+str(datetime.now())+"\n")


__main__()


