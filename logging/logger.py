import csv
import os
import datetime

#Session Variables
global currentSessionName
currentSessionName = 'Blank'
logFolder = "./Logs/"

def createNewLog():
    t = datetime.datetime.now()
    global currentSessionName
    currentSessionName = '{}_{}_{}-{}_{}_{}.csv'.format(t.day, t.month, t.year, t.hour, t.minute, t.second)
    if os.path.isfile(currentSessionName):
        print("Log: '{}' already exists, continuing log".format(currentSessionName))
    else:
        print('Created new Session: ' + currentSessionName)
        with open(logFolder + currentSessionName, 'w+') as f:
            f.write("HR,HRV,GSR\n")

def logDataPoint(hr,hrv,gsr):
    with open(logFolder + currentSessionName, 'a') as f:
        f.write("{},{},{},{}\n".format(datetime.datetime.now(),hr,hrv,gsr))

def logCustom(data):
    with open(logFolder + currentSessionName, 'a') as f:
        f.write("{},{}\n".format(datetime.datetime.now(),data))


createNewLog()
logDataPoint(1,0,0)
logDataPoint(2,0,0)
logDataPoint(3,0,0)
logDataPoint(4,0,0)
logDataPoint(5,0,0)
logCustom('Robot Task Started')
logDataPoint(1,0,0)
logDataPoint(1,0,0)
logDataPoint(1,0,0)
logDataPoint(1,0,0)
logDataPoint(1,0,0)
logDataPoint(1,0,0)
logCustom('Robot Task Ended')
logDataPoint(1,0,0)
logDataPoint(1,0,1)

