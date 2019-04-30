import csv
import os
import numpy as np
from misc import misc

numberOfTasks = 2
numberOfInitialQuestions = 5
numberOfQuestionPerTasks = 15
datapointsPerParticipants = numberOfQuestionPerTasks * numberOfTasks + numberOfInitialQuestions;

def evaluate():
    rawdata  = misc.getAllDataFromResultFolder()
    #participantMatrix = convertDataToParticipantMatrix(rawdata)     #Data can be accesssed by using data[Participant][Task][Specific attribute]
    #taskMatrix = convertToTaskMatrix(rawdata)

    #variance = calculateVariance(taskMatrix)
    #printData(variance)
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


