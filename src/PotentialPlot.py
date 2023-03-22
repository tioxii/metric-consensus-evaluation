import os
from statistics import mean

import numpy as np
import ImportCSVData as dt
from matplotlib import pyplot as plt, rc
import Potential as pot

CONFIGURATIONS = ['Random Positions', 'Random Clusters', 'Circle', '2-Choices']

def convertFileName(fileName : str) -> str:
    s = fileName.split('_POSITIONS')
    return ''.join(s)

def calculatePotential(path : str) -> float:
    data = dt.getData(path)

    rounds = dt.getElmentsAtIndex(data, 0)
    rounds = dt.getRounds(rounds)

    xval = dt.getXByRound(rounds[0], data)
    yval = dt.getYByRound(rounds[0], data)

    points = list(zip(xval,yval))
    return pot.potential(points)

def calculateConsensusTime(path : str) -> float:
    data = dt.getData(path)
    consensusTimes = list(map(lambda tup: float(tup[1]), data))
    return mean(consensusTimes)

def main():
    startingConfigurationsDirectory : str = 'results/potential/positions/'
    consensusTimeDirectory : str = 'results/potential/consensusTime/'

    startingConfFiles : list[str] = sorted(os.listdir(startingConfigurationsDirectory))
    startingConfFiles = startingConfFiles[0:10]
    consensusTimeFiles : list[str] = list(map(lambda f: convertFileName(f), startingConfFiles))

    files : list[tuple[str, str]] = list(zip(startingConfFiles, consensusTimeFiles))

    potentialData = []
    consensusTimeData = []

    for file in files:
        print(file)

        potential : float = calculatePotential(startingConfigurationsDirectory + file[0])
        consensusTime : float = calculateConsensusTime(consensusTimeDirectory + file[1])

        potentialData.append(potential)
        consensusTimeData.append(consensusTime)

    zipedData = list(zip(potentialData, consensusTimeData))

    print(np.corrcoef(potentialData, consensusTimeData))

    normalizedPotential : list[float] = list(map(lambda tup: tup[0] / tup[1], zipedData))
    simulation : list[int] = list(range(len(normalizedPotential)))
    #simulation = sorted(CONFIGURATIONS)

    rc('pgf', texsystem='pdflatex')
    rc('pgf', rcfonts=False)
    rc('font', **{'family': 'serif', 'serif': ['Palatino']})
    rc('text', usetex=True)

    fig, ax = plt.subplots()
    ax.plot(simulation, normalizedPotential, '.-')

    ax.set_xlabel(r'Simulation')
    ax.set_ylabel(r'Potential / Average Consensus Time')
    ax.set_title(r'Potential of the Closest Node Dynamics')
    #ax.set_ylim([1,1.5])

    plt.grid(True)
    plt.show()

    #fig.set_size_inches(5.1, 3.7)
    #fig.savefig('plots/' + potential + '.pgf')

if __name__ == '__main__':
    main()