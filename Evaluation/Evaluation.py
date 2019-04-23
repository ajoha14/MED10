import csv
import os
import numpy as np

numberOfTasks = 2
numberOfInitialQuestions = 5
numberOfQuestionPerTasks = 15
datapointsPerParticipants = numberOfQuestionPerTasks * numberOfTasks + numberOfInitialQuestions;

def evaluate():
    rawdata  = getAllDataFromResultFolder()
    #participantMatrix = convertDataToParticipantMatrix(rawdata)     #Data can be accesssed by using data[Participant][Task][Specific attribute]
    taskMatrix = convertToTaskMatrix(rawdata)

    variance = calculateVariance(taskMatrix)
    printData(variance)
    return 0

def calculateVariance(data):
    def variance(d):
        sumOfSquares = 0
        n = len(d)
        s = sum(d)
        for point in d:
            sumOfSquares = sumOfSquares + ((point - (s / n)) ** 2)
        v = sumOfSquares / (n - 1)
        return v


    result = []
    for row in data:
        result.append([row,variance(row)])

    return result

def convertToTaskMatrix(d):
    result = []
    for point in range(numberOfInitialQuestions, numberOfInitialQuestions + numberOfQuestionPerTasks):
        temp = []
        for participant in range(1, len(d)):
            temp.append(d[participant][point])
        result.append(temp)
    return result

def convertDataToParticipantMatrix(rawData):
    def formatData(d,start):
        dataLine = [d[start:start + numberOfInitialQuestions]]
        for step in range(0,numberOfTasks):
            x = step * numberOfQuestionPerTasks
            newline = d[start + x + numberOfInitialQuestions : start + x + numberOfInitialQuestions + numberOfQuestionPerTasks]
            dataLine.append(newline)
        return dataLine

    result = []
    for participant in rawData:
        result.append(formatData(participant,0))
    return result

def printData(data):
    for row in data:
        print(row)

def getAllDataFromResultFolder(seperator = ','):
    def convertToNumber(string):
        if str.isdigit(string): return float(string)
        else: return string

    data = []
    dirc = os.path.dirname(os.path.abspath("__file__")).replace("\\", "/") + "/Evaluation/Results/"
    for file in os.listdir(dirc):
        if file.endswith(".csv"):
            print("Opening file: '" + str(file) + "'")
            with open(dirc+file, 'rt') as f:
                reader = csv.reader(f, delimiter=seperator, skipinitialspace=True)
                if not data:
                    for col in reader:
                        data.append(col)
                else:
                    data.append([row for idx, row in enumerate(reader) if idx == 1][0])
            continue
        else:
            continue
    for participant in range(0,len(data)):
        for datapoint in range(0,len(data[participant])):
            data[participant][datapoint] = convertToNumber(data[participant][datapoint])
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
