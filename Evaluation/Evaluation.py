import csv
import numpy as np

def getDataFromFile(file, seperator = ','):
    data = []
    print("Opening file: '" + str(file) + "'")
    with open(file, 'rt') as f:
        reader = csv.reader(f, delimiter=seperator, skipinitialspace=True)
        for col in reader:
            #item = float(col[1])
            data.append(col)
    #data = np.asarray(data)
    return data


#{ } [ ]
def convertDataToMatrix(data):
    def extractTaskData(data, begin, end):
        temp = []
        for x in range(begin, end):
            temp.append(data[1][x])
        return temp

    rows = len(data[:]); cols = len(data[0])
    print("rows,cols = [" + str(rows)+","+str(cols) + "]")

    #listOfMatrixes = [ ]
    #dataMatrix = np.zeros((rows,cols))
    #dataMatrix = [[0 for x in range(9)] ,[0 for y in range(cols)]]
    dataMatrix = [[] ,[]]
    dataMatrix[0].append("Initial");    dataMatrix[0].append("Task 1")
    dataMatrix[0].append("Task 2");      dataMatrix[0].append("Task 3");
    dataMatrix[0].append("Task 7");    dataMatrix[0].append("Task 5");
    dataMatrix[0].append("Task 6");    dataMatrix[0].append(" Task 7");
    dataMatrix[0].append("Task 8");
    #Initial
    dataMatrix[1].append(extractTaskData(data,1,5))
    #Task
    dataMatrix[1].append(extractTaskData(data,5,5+8))
    print(dataMatrix)