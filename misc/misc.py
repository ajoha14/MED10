import csv
import os

def printData(data):
    for row in data:
        print(row)

def getAllDataFromResultFolder(seperator = ','):
    def convertToNumber(string):
        if str.isdigit(string): return float(string)
        else: return string

    data = []
    dirc = os.path.dirname(os.path.abspath("__file__")).replace("\\", "/") + "/Evaluation/Results/"
    for directory in os.listdir(dirc):
        for file in directory:
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
    print(data)
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

def saveToFile(file,d):
    with open(file, 'w') as f:
        for it in range(0,len(d)):
            for y in range(0,len(d[it])):
                f.write(d[it][y])
                if y is not len(d[it])-1:
                    f.write(",")
            f.write("\n")