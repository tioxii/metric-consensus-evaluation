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
        ax.plot(participants, roundsMean, label=str(val))

def convertToDiagramSingle(data : list[tuple], ax):
    participants = dt.getElmentsAtIndex(data, 0)
    participants = list(map(lambda x: int(x), participants))
    participants = sorted(set(participants))
    roundsMean = mapToAverage(participants, data)
    #Create graph
    return ax.plot(participants, roundsMean)

def main():
    isAllInSingleFile = False

    #Files
    path = "results/06-12-2022_13-02-49_R-100_SYNC-true.csv" # Base plot
    data = dt.getData(path)
    
    path2 = "results/FullCircle_R-100_SYNC-true.csv" # Full circle
    data2 = dt.getData(path2)
    
    path3 = "results/TwoFarAway_R-100_SYNC-true.csv"
    data3 = dt.getData(path3)

    #Figure
    fig, ax = plt.subplots()

    #Data
    if len(data[0]) > 2 and isAllInSingleFile:
        group = dt.getElmentsAtIndex(data, 2)
        group = sorted(set(group))
        convertToDiagram(group, data, ax)
    else:
        l, = convertToDiagramSingle(data, ax)
        g, = convertToDiagramSingle(data2, ax)
        f, = convertToDiagramSingle(data3, ax)
        l.set_label("All Random")
        g.set_label("Full Circle")
        f.set_label("Two Far Away (100)")
        

    #Plot
    ax.set_ylim([0,6])
    ax.set_xscale('log')
    ax.grid(True)
    ax.set_title('Beta-Analysis (Synchronous)')
    ax.set_xlabel('Participants')
    ax.set_ylabel('Rounds / log(Participants)')
    ax.legend()

    plt.show()

if __name__ == "__main__":
    main()
