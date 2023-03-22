import os
from matplotlib import rc
import matplotlib.pyplot as plt
import numpy as np
import ImportCSVData as dt

def getConvergedPosition(path : str) -> tuple:
    data = dt.getData(path)

    rounds = dt.getElmentsAtIndex(data, 0)
    rounds = dt.getRounds(rounds)

    maxRound = max(rounds)

    xVal = dt.getXByRound(maxRound, data)[0]
    yVal = dt.getYByRound(maxRound, data)[0]

    return (xVal, yVal)

def main():
    directoryPath : str = 'potential/positions/'

    files : list[str] = sorted(os.listdir(directoryPath))

    convergedPositions : tuple = []

    for file in files:
        convergedPosition = getConvergedPosition(directoryPath + file)
        convergedPositions.append(convergedPosition)
        print(convergedPosition)

    xData = list(map(lambda x: x[0], convergedPositions))
    yData = list(map(lambda x: x[1], convergedPositions))

    heatmap, xedges, yedges = np.histogram2d(xData, yData, bins=10)
    extent = [0, 1, 0, 1]

    rc('font', **{'family': 'serif', 'serif': ['Palatino']})
    rc('text', usetex=True)

    fig, ax = plt.subplots()
    l = ax.imshow(heatmap.T, extent=extent, origin='lower')
    fig.colorbar(l, ax=ax)
    
    ax.set_title('Heatmap of converged opinions')
    ax.set_xlabel('x-Axis')
    ax.set_ylabel('y-Axis')
    plt.show()

if __name__ == '__main__':
    main()