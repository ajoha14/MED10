import csv
import numpy as np

numberOfTasks = 1
numberOfInitialQuestions = 4
numberOfQuestionPerTasks = 15
datapointsPerParticipants = numberOfQuestionPerTasks * numberOfTasks + numberOfInitialQuestions;


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
    rows = len(data[:]); cols = len(data[0])
    print("rows,cols = [" + str(rows)+","+str(cols) + "]")
    print(datapointsPerParticipants)

    p = Participant()
    p.loadData(data,1)
    p.loadData(data,1)
    #p.loadData(data,1,1)

    print(p.dataMatrix)

class Participant:
    def __init__(self):
        self.dataMatrix = []


    def loadData(self,data,start):
        print(data)
        self.dataMatrix.append(data[1][start:start + numberOfInitialQuestions])
        #line below should iterate through each task and append for each task. Then it is done
        self.dataMatrix.append(data[1][start + numberOfInitialQuestions:start + numberOfInitialQuestions + numberOfQuestionPerTasks])
