import csv
import os
import numpy as np

numberOfTasks = 2
numberOfInitialQuestions = 5
numberOfQuestionPerTasks = 15
datapointsPerParticipants = numberOfQuestionPerTasks * numberOfTasks + numberOfInitialQuestions;

def evaluate():
    rawdata  = getAllDataFromResultFolder()
    data = convertDataToMatrix(rawdata)     #Data can be accesssed by using data[Participant][Task][Specific attribute]
    '''
    print(data[0])
    print(data[1])
    print(data[2])
    '''
    variance = calculateVariance(data)
    return 0

def calculateVariance(data):
    result = []
    """
    print(data[1])
    print(data[1][2])
    print(len(data[1][1]))
    
    p = 1
    t = 1
    n = len(data[p][t])
    s = sum(data[p][t])
    print(data[p][t])
    print(s)
    print(s/n)
    totalsumOfSquares = 0
    for point in range(0, len(data[p][t])):
        sumOfSquares = sumOfSquares + ((data[p][t][point] - (s/n)) ** 2)

    variance = totalsumOfSquares / (n-1)
    print(variance)
    """
    for question in range(1,15):
        for task in range(1,2):
            #calculate varience
            n = len(data[1][1])
            sumOfSquares = 0
            average = sum(data[:][task][question]) / n
            print(average)
            #for participant in range(0,len(data)):

            #sumOfSquares = (data[:][task][question]-average)**2
            print(sumOfSquares)
            result.append(sumOfSquares/(n-1))

    """
    print(result[0][0])
    print(result[0][1])
    print(result[1][0])
    print(result[1][1])

    print(len(result[0]))
    print(len(result[1]))
    """
    return result

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
        for step in range(0,numberOfTasks):
            x = step * numberOfQuestionPerTasks
            newline = d[start + x + numberOfInitialQuestions : start + x + numberOfInitialQuestions + numberOfQuestionPerTasks]
            dataLine.append(newline)
        return dataLine

    def convertToInt(data):
        r = data
        for x in range(0,len(data)):
            for y in range(0,len(data[x])):
                for z in range(0,len(data[x][y])):
                    try:
                        r[x][y][z] = int(r[x][y][z])
                    except Exception as e:
                        #e.with_traceback(None)
                        continue
        return r

    result = []
    for participant in rawData:
        result.append(formatData(participant,0))
    result = convertToInt(result)
    return result
