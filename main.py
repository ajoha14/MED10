import argparse
from misc import misc
import csv
import numpy as np
from numpy.distutils.system_info import f2py_info
from Signals.ArduinoSerialPortCommunicator import SerialReader
from misc.logging import Logger
import misc.logging as logging
from misc.buffer import Buffer
import Evaluation.Evaluation as Eval
import misc.QuickMaths as math
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
    #worker.EstablishBaseline()
    worker.RecordData()
    #worker.evaluate()

class latinSquare:
    d = misc.getDataFromFile("Evaluation/latinSquare.txt")
    water = d[0]
    lego = d[1]
    square = []

    def __init__(self):
        self.square.append(self.water.copy())
        temp = self.square[0].pop(0)
        self.square[0].append(temp)
        self.square.append(self.lego.copy())
        temp = self.square[1].pop(0)
        self.square[1].append(temp)

    def SaveState(self):
        misc.saveToFile("Evaluation/latinSquare.txt", self.square)

class Worker:
    looping = True
    def __init__(self):
        self.gsrbuffer = Buffer(1200)
        self.hrbuffer = Buffer(1200)
        self.log = Logger()
        """ls = latinSquare()
        for x in ls.square:
            print(x)
        ls.SaveState()"""

        print("worker started")

    def plotstuff(self):
        plt.figure(1)
        while True:
            plt.plot(self.gsrbuffer.data)
            plt.plot(self.hrbuffer.data)

    def EstablishBaseline(self):
        serialport = SerialReader(port='COM5')
        keyboard.add_hotkey('space', self.toogleLoop, args=())
        first = False
        if serialport.ser is not None:
            print("Establishing baseline...")
            while self.looping:
                currentData = serialport.current_data()
                if currentData is not 'error':
                    try:
                        time, gsr, hr = currentData.split(',', 3)
                        gsr, hr = float(gsr), float(hr)
                        self.gsrbuffer.add(gsr)
                        self.hrbuffer.add(hr)
                        if self.gsrbuffer.isFull():
                            if not first:
                                first = True
                                print("Baseline established!")
                                break
                        self.log.logString(currentData)
                    except:
                        self.log.logString(currentData)

    def RecordData(self):
        serialport = SerialReader(port='COM5')
        keyboard.add_hotkey('space', self.toogleLoop, args=())
        if serialport.ser is not None:
            while self.looping:
                currentData = serialport.current_data()
                if currentData is not 'error':
                    try:
                        self.log.logString(currentData)
                    except:
                        self.log.logString(currentData)

    def plotstuff(self):
        while True:
            plt.figure(1)
            plt.plot(self.gsrbuffer.data)
            #plt.plot(self.hrbuffer.data)
            plt.show()
            plt.pause(0.05)

    def AnalyseTestData(self):
        print("Arduino not plugged in. Loading data from log instead")
        gsrList = logging.getGSRFromLog("Logs/03_27-09_04_33.csv")
        print(gsrList)
        mean = math.moving_average(gsrList,100)
        #slope = math.slope_of(mean)
        slopeMovingAverage = math.slope_window(mean, 30)
        plt.figure(1)
        plt.plot(gsrList)
        plt.figure(2)
        plt.plot(mean)
        #plt.figure(3)
        #plt.plot(slope)
        plt.figure(4)
        plt.plot(slopeMovingAverage)
        plt.show()

    def toogleLoop(self):
        print("Making data key point")
        #self.looping = not self.looping
        self.log.logString("TEST KEY FRAME")

    def evaluate(self):
        p = Eval.evaluate()
        #print("Ttest result = ")
        print(p)

__main__()

