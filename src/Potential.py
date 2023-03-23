import math
from statistics import mean, stdev

from matplotlib import pyplot as plt
import ImportCSVData as dt

def calcDistanceEuclidean2D(firstPoint : tuple, secondPoint : tuple) -> float:
    firstCoord : float = firstPoint[0] - secondPoint[0]
    secondCoord : float = firstPoint[1] - secondPoint[1]
    return math.sqrt(pow(firstCoord, 2) + pow(secondCoord, 2))

def doesWinAgainstFor(price : tuple[float, float], firstContestor : tuple[float, float], secondContestor : tuple) -> bool:
    if(calcDistanceEuclidean2D(price, firstContestor) >= calcDistanceEuclidean2D(price, secondContestor)):
        return False
    if(calcDistanceEuclidean2D(price, firstContestor) == 0):
        return False
    return True

def calcPotentialForPoint(point : tuple, otherPoints : list[tuple]) -> int:
    counter : int = 0
    for p1 in otherPoints:
        for p2 in otherPoints:
            if(doesWinAgainstFor(p1, point, p2)):
                counter += 1
    return counter

def calcPotentialForConfiguration(data) -> list:
    return list(map(lambda x: calcPotentialForPoint(x, data), data))

def potential(points : list[tuple[float, float]]) -> float:
    numberOfPoints = len(points)
    result = calcPotentialForConfiguration(points)
    print(result)
    potential = (mean(result) - stdev(result)) / numberOfPoints
    return potential

def main():
    path = 'results/potentialSpecific/positions/Random Nodes_R-100_SYNC-true_POSITIONS.csv'
    data = dt.getData(path)

    #3571.8849214112233 for Circle1000

    rounds = dt.getElmentsAtIndex(data, 0)
    rounds = dt.getRounds(rounds)

    potentials = []

    round : int = 0

    xval = dt.getXByRound(rounds[round], data)
    yval = dt.getYByRound(rounds[round], data)
    points = list(zip(xval,yval))
    print(potential(points))

    plt.subplots()

    

if __name__ == '__main__':
    main()