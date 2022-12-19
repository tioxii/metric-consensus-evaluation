import matplotlib.pyplot as plt
import ImportCSVData as dt
from numpy import log
from statistics import mean
from statistics import stdev

#Normalize for synchronous process.
def normalize(n : int, round : int) -> float:
    return round / log(n)

#Calculate mean.
def calculateMean(n : int, rounds : list[tuple]) -> float:
    filteredList = list(filter(lambda x: int(x[0]) == n, rounds))
    filteredList = list(map(lambda x: normalize(n, int(x[1])), filteredList))
    average = mean(filteredList)
    return average

#Calculate standard deviation.
def calculateStandardDeviation(n : int, rounds : list[tuple]) -> list[float]:
    filteredList = list(filter(lambda x: int(x[0]) == n, rounds))
    filteredList = list(map(lambda x: normalize(n, int(x[1])), filteredList))
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
        ax.plot(participants, roundsMean, label='Synchronous')

def convertToDiagramSingle(data : list[tuple], ax):
    participants = dt.getElmentsAtIndex(data, 0)
    participants = list(map(lambda x: int(x), participants))
    participants = sorted(set(participants))
    roundsMean = mapToAverage(participants, data)
    #Create graph
    ax.plot(participants, roundsMean, label='Synchronous')

def main():
    isAllInSingleFile = False
    colors = ['blue', 'orange', 'green', 'red']
    
    #Files
    path = "results/06-12-2022_13-02-49_R-100_SYNC-true.csv" # Base plot
    data = dt.getData(path)
    
    path2 = ""
    data2 = dt.getData(path2)

    path3 = ""
    data3 = dt.getData(path3)
    
    #Figure
    fig, ax = plt.subplots()

    #Data
    if len(data[0]) > 2 and isAllInSingleFile:
        group = dt.getElmentsAtIndex(data, 2)
        group = sorted(set(group))
        #convertToDiagram(group, data, ax)
    else:
        convertToDiagramSingle(data, ax)
        convertToDiagramSingle(data2, ax)
        convertToDiagramSingle(data3, ax)
        
    #Plot
    ax.set_ylim([0,6])
    ax.set_xscale('log')
    ax.grid(True)
    ax.set_title('Synchronous Metric Consensus Process')
    ax.set_xlabel('Participants')
    ax.set_ylabel('Rounds / log(Participants)')

    plt.show()

if __name__ == "__main__":
    main()
