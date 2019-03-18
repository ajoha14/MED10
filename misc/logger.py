import csv
import os
import datetime

#Session Variables
from itertools import count

global currentSessionName
currentSessionName = 'Blank'
logFolder = "./Logs/"


def create_new_log(path=None):
    global currentSessionName
    if path is None:
        t = datetime.datetime.now()
        currentSessionName = logFolder + '{}_{}_{}-{}_{}_{}.csv'.format(t.day, t.month, t.year, t.hour, t.minute, t.second)
    else:
        currentSessionName = path

    if os.path.isfile(currentSessionName):
        print("Log: '{}' already exists, continuing log".format(currentSessionName))
    else:
        print('Created new Session: ' + currentSessionName)
        with open(currentSessionName, 'w+') as f:
            f.write("TIMESTAMP,HR,HRV,GSR\n")


def log_data_point(hr, hrv, gsr):
    with open(currentSessionName, 'a') as f:
        f.write("{},{},{},{}\n".format(datetime.datetime.now(), hr, hrv, gsr))


def log_custom(data):
    with open(currentSessionName, 'a') as f:
        f.write("{},{}\n".format(datetime.datetime.now(), data))

def get_data_from_log(log):
    data = []
    with open(log, 'rt') as f:
        reader = csv.reader(f, delimiter=',', skipinitialspace=True)
        cols = next(reader)
        for col in cols:
            data.append(col)
    return data
