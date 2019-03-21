import csv
import os
from datetime import datetime

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
            time = datetime.utcnow().strftime('%m_%d-%H_%M_%S.%f')
            f.write("{},{},{},{}\n".format(time, hr, hrv, gsr))

    def logString(self, data):
        with open(self.currentSessionName, 'a') as f:
            time = datetime.utcnow().strftime('%m_%d-%H_%M_%S.%f')
            f.write("{},{}\n".format(time, data))

    @staticmethod
    def getDataFromLog(log):
        data = []
        print("opening " + str(log))
        with open(log, 'rt') as f:
            reader = csv.reader(f, delimiter=',', skipinitialspace=True)
            for col in reader:
                print(col)
                data.append(col)
        return data
