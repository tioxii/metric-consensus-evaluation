import ImportCSVData as dt
import numpy as np
import matplotlib.pyplot as plt

def calculateMeanForRound(r : int, data):
    xdata = dt.getXByRound(r, data)
    ydata = dt.getYByRound(r, data)
    xmean = np.mean(xdata)
    ymean = np.mean(ydata)
    return (xmean, ymean)

def main():
    file = 'positions/Circle100_R-1_SYNC-true_POSITIONS.csv'
    data = dt.getData(file)

    rounds = dt.getElmentsAtIndex(data, 0)
    rounds = dt.getRounds(rounds)
    print(rounds)

    meanOfEachRound : list[tuple[float, float]] = list(map(lambda r: calculateMeanForRound(r, data), rounds))
    x = list(map(lambda x: x[0], meanOfEachRound))
    y = list(map(lambda y: y[1], meanOfEachRound))

    fig, ax = plt.subplots()
    l, = ax.plot(x, y, '.-', color='orange')
    ax.set_xlim([0,1])
    ax.set_ylim([0,1])
    plt.grid()
    plt.show()
    
if __name__ == '__main__':
    main()