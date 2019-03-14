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