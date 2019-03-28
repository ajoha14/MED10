import csv
import os
from datetime import datetime
from misc.buffer import Buffer

def getDataFromLog(log):
    data = []
    print("Opening file: '" + str(log) + "'")
    with open(log, 'rt') as f:
        reader = csv.reader(f, delimiter=',', skipinitialspace=True)
        for col in reader:
            data.append(col)
    return data

def getHRFromLog(log):
    data = Buffer()
    print("Opening file: '" + str(log) + "'")
    with open(log, 'rt') as f:
        reader = csv.reader(f, delimiter=',', skipinitialspace=True)
        for col in reader:
            try:
                item = int(col[2])
                data.add(item)
            except ValueError as e:
                print(e)
    return data

def getGSRFromLog(log):
    data = []
    first = True
    print("Opening file: '" + str(log) + "'")
    with open(log, 'rt') as f:
        reader = csv.reader(f, delimiter=',', skipinitialspace=True)
        i=0
        for col in reader:
            if first:
                first = False
                continue
            item = float(col[1])
            data.append(item)
            i = i + 1
    return data

def getTimestampFromLog(log):
    data = []
    print("Opening file: '" + str(log) + "'")
    with open(log, 'rt') as f:
        reader = csv.reader(f, delimiter=',', skipinitialspace=True)
        for col in reader:
            item = col[0]
            data.append(item)
    return data


class Logger:
    def __init__(self, path=None):
        self.currentSessionName = 'Blank'
        self.logFolder = "./Logs/"
        if path is None:
            self.currentSessionName = self.logFolder + datetime.utcnow().strftime('%m_%d-%H_%M_%S')+'.csv'
        else:
            self.currentSessionName = path
        if os.path.isfile(self.currentSessionName):
            print("Log '{}' already exists, continuing log".format(self.currentSessionName))
        else:
            print('Created new Session: ' + self.currentSessionName)
            with open(self.currentSessionName, 'w+') as f:
                f.write("TIMESTAMP,HR,HRV,GSR\n")

    def logDataPoint(self, hr, hrv, gsr):
        with open(self.currentSessionName, 'a') as f:
            f.write("{},{},{}\n".format(hr, hrv, gsr))

    def logString(self, data):
        with open(self.currentSessionName, 'a') as f:
            f.write(data + "\n")


