from ast import List
import csv

def getData(file_name):
    file = open(file_name)
    type(file)
    csvreader = csv.reader(file)
    
    rows = []
    for row in csvreader:
        rows.append(row)

    file.close()
    return rows

def getElmentsAtIndex(data, index : int):
    result = map(lambda x: x[index], data)
    return result

def getRounds(rounds):
    result = map(lambda x: int(x), rounds)
    return sorted(set(result))

def getXByRound(round : int, data):
    result = list(filter(lambda x: int(x[0]) == round, data))
    result = list(getElmentsAtIndex(result, 1))
    result = map(lambda x: float(x), result)
    return list(result)

def getYByRound(round : int, data):
    result = list(filter(lambda x: int(x[0]) == round, data))
    result = list(getElmentsAtIndex(result, 2))
    result = map(lambda x: float(x), result)
    return list(result)

def compareTuple(tupleOne : tuple, tupleTwo : tuple):
    result = True
    for i in range(len(tupleOne)):
        result = result and (tupleOne[i] == tupleTwo[i])
    return result


def getClusterSize(position, positions):
    filtered = list(filter(lambda x: compareTuple(x, position), positions))
    return len(filtered)

def getClusterSizes(positions): #TODO
    pos_set = sorted(set(positions))
    return list(map(lambda x: getClusterSize(x, positions), pos_set))