import re
import ImportCSVData as dt
import matplotlib.pyplot as plt
from matplotlib import rc

__TERMINATION_CONSTANT = 10000
__synchronous : bool = True

def lookForGroup(val : float, tup : tuple, index : int) -> bool:
    if(round(float(tup[index]), 2) == val):
        return True
    return False

def calculatePercantage(n : int, lst : list, synchronous : bool) -> float:
    group = list(filter(lambda tup: lookForGroup(float(n), tup, 0), lst))
    counter : float = 0

    for element in group:
        if(synchronous and int(element[1]) < __TERMINATION_CONSTANT):
            counter += 1
        if((not synchronous) and int(element[1]) < __TERMINATION_CONSTANT * n):
            counter += 1

    return round(float(counter / len(group)), 4)

def transformData(path : str) -> list:
    data = dt.getData(path)

    synchronousStr : str = re.split('(.*)(SYNC-)(.*)(\.csv)', path)[3]
    if(synchronousStr == 'true'):
        synchronous = True
    if(synchronousStr == 'false'):
        synchronous = False

    groups : list = sorted(set(dt.getElmentsAtIndex(data, 2)))
    groups = sorted(map(lambda x: round(float(x), 2), groups))

    resultList : list = []
    for element in groups:
        element = float(element)
        group = list(filter(lambda tup: lookForGroup(element, tup, 2), data))
        nodes = list(sorted(set(map(lambda tup: int(tup[0]), group))))
        for n in nodes:
            result = (element, calculatePercantage(n, group, synchronous), n)
            resultList.append(result)

    return resultList

def main():
    rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
    rc('text', usetex=True)

    ax = plt.subplot()

    path : str = 'results/Stability-Analysis/ClosestToMeanStability_R-100_SYNC-false.csv'
    transformedData = transformData(path)
    
    n_set : list = sorted(set(map(lambda tup: tup[2], transformedData)))
    for n in n_set:
        filteredData = list(filter(lambda tup: int(tup[2]) == int(n), transformedData))
        xData = list(map(lambda tup: tup[0], filteredData))
        yData = list(map(lambda tup: tup[1], filteredData))
        ax.plot(xData, yData, label=str(n))

    ax.set_xlabel(r'$\approx$ Fraction of dishonest nodes')
    ax.set_ylabel(r'$\approx$ Fraction of corrupted consensus processes')
    ax.set_title('Stability - Closest to Mean - Asynchronous')
    ax.grid()
    plt.show()

if __name__ == '__main__':
    main()