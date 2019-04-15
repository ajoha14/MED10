import csv
import os
import numpy as np

numberOfTasks = 2
numberOfInitialQuestions = 5
numberOfQuestionPerTasks = 15
datapointsPerParticipants = numberOfQuestionPerTasks * numberOfTasks + numberOfInitialQuestions;

def Ttest():
    #Data can be accesssed by using data[Participant][Task][Specific attribute]
    data = getdata()
    return 0


def getdata():
    rawdata  = getAllDataFromResultFolder()
    data = convertDataToMatrix(rawdata)
    return data
def getAllDataFromResultFolder(seperator = ','):
    def isEmpty(lst):
        if lst:
            return False
        else:
            return True
    data = []
    dirc = os.path.dirname(os.path.abspath("__file__")).replace("\\", "/") + "/Evaluation/Results/"
    for file in os.listdir(dirc):
        if file.endswith(".csv"):
            print("Opening file: '" + str(file) + "'")
            with open(dirc+file, 'rt') as f:
                reader = csv.reader(f, delimiter=seperator, skipinitialspace=True)
                if isEmpty(data):
                    for col in reader:
                        data.append(col)
                else:
                    data.append([row for idx, row in enumerate(reader) if idx == 1][0])
            continue
        else:
            continue
    print()
    return data

def getDataFromFile(file, seperator = ','):
    data = []
    print("Opening file: '" + str(file) + "'")
    with open(file, 'rt') as f:
        reader = csv.reader(f, delimiter=seperator, skipinitialspace=True)
        for col in reader:
            data.append(col)
    #data = np.asarray(data)
    return data

def convertDataToMatrix(rawData):
    def formatData(d,start):
        dataLine = [d[start:start + numberOfInitialQuestions]]
        #"2019", "Son of god", "Right hand of god", "1"

        #go through the data in steps of 15 to store each task datapoints as a new dimension
        for step in range(0,len(rawData[1]),15):
            dataLine.append(d[start + step + numberOfInitialQuestions : start + step + numberOfInitialQuestions + numberOfQuestionPerTasks])
            #"1","2","3","4","5","6","3","6","5","4","2","4","5","2","1"
        return dataLine

    numberofParticipants = len(rawData[:]); dpPerPart = len(rawData[1])
    print("numberofParticipants, dpPerPart  = [" + str(numberofParticipants)+","+str(dpPerPart) + "]")
    if datapointsPerParticipants is not dpPerPart:
        print("ERROR: The number of datapoints per participants does not match the expected number of datapoints.")

    result = []
    for participant in rawData:
        result.append(formatData(participant,0))

    return result
