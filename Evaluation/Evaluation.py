import csv


def getDataFromFile(file, seperator = ','):
    data = []
    print("Opening file: '" + str(file) + "'")
    with open(file, 'rt') as f:
        reader = csv.reader(f, delimiter=seperator, skipinitialspace=True)
        i=0
        for col in reader:
            item = float(col[1])
            data.append(item)
            i = i + 1
    return data

def printData(data):
    for x in data:
        print(x)
