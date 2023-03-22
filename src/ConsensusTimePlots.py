import os
import re
from matplotlib import rc
from matplotlib.axes import Axes
import matplotlib.pyplot as plt
import ImportCSVData as dt
from numpy import log
from statistics import mean
from statistics import stdev

#Calculate mean.
def calculateMean(n : int, rounds : list[tuple]) -> float:
    filteredList = list(filter(lambda x: int(x[0]) == n, rounds))
    filteredList = list(map(lambda x: x[1], filteredList))
    average : float = mean(filteredList)
    return average

#Calculate standard deviation.
def calculateStandardDeviation(n : int, rounds : list[tuple]) -> list[float]:
    filteredList = list(filter(lambda x: int(x[0]) == n, rounds))
    filteredList = list(map(lambda x: x[1], filteredList))
    deviation = stdev(filteredList)
    return deviation

#Map each participant number to the average of all simulation rounds with this number of participants
def mapToAverage(participants : list[int], data : list[tuple]) -> list[float]:
    subList = list(map(lambda p: calculateMean(p, data), participants))
    return subList

#Map each participant number to the standard deviation of all simulation round with this number of participants
def mapToStandardDeviation(participants : list[int], data : list[tuple]) -> list[float]:
    subList = list(map(lambda p: calculateStandardDeviation(p, data), participants))
    return subList

def convertToDiagram(group : list, data : list[tuple], ax):
    for val in group:
        #Filter data by third row
        filteredData = list(filter(lambda x: x[2] == val, data))
        #Calculate Values
        participants = dt.getElmentsAtIndex(filteredData, 0)
        participants = list(map(lambda x: int(x), participants))
        participants = sorted(set(participants))
        roundsMean = mapToAverage(participants, filteredData)
        #Create graph
        ax.plot(participants, roundsMean, label=str(val))


#Normalize for synchronous process. #log(n) - log(log(n)) for full circle
def normalize(n : int, consensusTime : int, synchronous : bool) -> float:
    if(synchronous):
        return consensusTime / (log(n))
    else:
        return consensusTime / (n * log(n))

#Normalize Data
def normalizeData(data : tuple, synchronous : bool):
    for tupe in data:
        tupe[0] = int(tupe[0])
        tupe[1] = normalize(tupe[0], int(tupe[1]), synchronous)

def transform(path : str, ax : Axes, fileName : str):
    data = dt.getData(path)
    
    synchronousStr : str = re.split('(.*)(SYNC-)(.*)(\.csv)', path)[3]

    if(synchronousStr == 'true'):
        synchronous = True
    else:
        synchronous = False

    normalizeData(data, synchronous)
    participants = sorted(set(dt.getElmentsAtIndex(data, 0)))
    #roundsStdev = mapToStandardDeviation(participants, data)
    roundsMean = mapToAverage(participants, data)
    l, = ax.plot(participants, roundsMean, label= 'Synchronous' if synchronous else 'Asynchronous ')
    return l

def plotSettings(ax : Axes, dirName : str):
    ax.set_ylim([0,10])
    ax.set_xscale('log')
    ax.grid(True)
    ax.set_title(r'' + dirName)
    ax.set_xlabel(r'Number of Nodes $n$')
    ax.set_ylabel(r'Normalized Consensus Time')
    ax.legend() 

def createDiagrammFromDirectory(path : str, shouldSave : bool = False):
    dirName = os.path.dirname(path)
    files = os.listdir(path)
    fig, ax = plt.subplots()
    lines = list(map(lambda x: transform(path + x, ax, x), files))
    
    #for i in range(len(lines)):
    #    label = re.split("(_.*)", files[i])[0]
    #    lines[i].set_label(label)

    dirName = re.split("(/)", dirName)[4]

    plotSettings(ax, dirName)
    if(shouldSave):
        fig.set_size_inches(5.1, 3.7)
        fig.savefig('plots/' + dirName + '.pgf')
    else:
        plt.show()
    
def createDiagrammFromFile(path : str):
    fileName = os.path.basename(path)
    data = dt.getData(path)
    if(len(data[0])):
        fig, ax = plt.subplots()
        normalizeData(data)
        group = dt.getElmentsAtIndex(data, 2)
        group = sorted(set(group))
        convertToDiagram(group, data, ax)
        title = re.split("(_.*)", fileName)[0]
        plotSettings(ax, title)

def createAllDiagramms():
    direc = 'results/consensusTime/'
    directories = os.listdir(direc)

    for dir in directories:
        createDiagrammFromDirectory(direc + dir + '/', True)

def createSingleDiagramm(file : str):
    direc = 'results/consensusTime/'
    file += '/'
    path = direc + file
    isDirectory = os.path.isdir(path)
    isFile = os.path.isfile(path)

    if(isDirectory):
        createDiagrammFromDirectory(path, False)
    if(isFile):
        createDiagrammFromFile(path)

def main():
    rc('pgf', texsystem='pdflatex')
    rc('pgf', rcfonts=False)
    rc('font', **{'family': 'serif', 'serif': ['Palatino']})
    rc('text', usetex=True)

    file : str = 'Random Clusters - Closest Node'
    shouldCreateAll : bool = False

    if(shouldCreateAll):
        createAllDiagramms()
    else:
        createSingleDiagramm(file)

if __name__ == "__main__":
    main()
