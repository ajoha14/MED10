import csv
import os

def printData(data):
    for row in data:
        print(row)

def getAllDataFromResultFolder(participant = "Evaluation/Results/",seperator = ','):
    def convertToNumber(string):
        if str(string).replace(".","").isdigit():return float(string)
        else:return string
    result =[]
    dirc = os.path.dirname(os.path.abspath("__file__")).replace("\\", "/") + "/" + participant
    for file in os.listdir(dirc):
        if file.endswith(".csv"):
            data = [[], [], []]
            print("Opening file: '" + str(file) + "'")
            with open(file, 'rt') as f:
                reader = csv.reader(f, delimiter=seperator, skipinitialspace=True)
                for col in reader:
                    data[0].append(convertToNumber(col[0]))
                    data[1].append(convertToNumber(col[1]))
                    data[2].append(convertToNumber(col[2]))
        result.append(data)
    return result

def getDataFromFile(file, seperator = ','):
    def convertToNumber(string):
        if str(string).replace(".","").isdigit():return float(string)
        else:return string
    data = [[],[],[],[]]
    index = 0
    print("Opening file: '" + str(file) + "'")
    with open(file, 'rt') as f:
        reader = csv.reader(f, delimiter=seperator, skipinitialspace=True)
        for col in reader:
            index = index + 1
            try:
                data[0].append(convertToNumber(col[0]))
                data[1].append(convertToNumber(col[1]))
                data[2].append(convertToNumber(col[2]))
            except Exception as e:
                continue
            if len(col) is not 3:
                data[3].append(index)

    return data

def saveToFile(file,d):
    with open(file, 'w') as f:
        for it in range(0,len(d)):
            for y in range(0,len(d[it])):
                f.write(d[it][y])
                if y is not len(d[it])-1:
                    f.write(",")
            f.write("\n")