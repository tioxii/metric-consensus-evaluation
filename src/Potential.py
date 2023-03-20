import math
from statistics import mean, stdev
import ImportCSVData as dt

def calcDistanceEuclidean2D(firstPoint : tuple, secondPoint : tuple) -> float:
    firstCoord : float = firstPoint[0] - secondPoint[0]
    secondCoord : float = firstPoint[1] - secondPoint[1]
    return math.sqrt(pow(firstCoord, 2) + pow(secondCoord, 2))

def doesWinAgainstFor(price : tuple[float, float], firstContestor : tuple[float, float], secondContestor : tuple) -> bool:
    if(calcDistanceEuclidean2D(price, firstContestor) < calcDistanceEuclidean2D(price, secondContestor)):
        return True
    return False

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
    potential = (mean(result) - stdev(result)) / numberOfPoints
    return potential

def main():
    path = 'positions/12-12-2022_10-46-16_R-1_SYNC-true_POSITIONS.csv'
    data = dt.getData(path)

    #3571.8849214112233 for Circle1000

    rounds = dt.getElmentsAtIndex(data, 0)
    rounds = dt.getRounds(rounds)

    xval = dt.getXByRound(rounds[0], data)
    yval = dt.getYByRound(rounds[0], data)
    points = list(zip(xval,yval))
    print(potential(points))
    

if __name__ == '__main__':
    main()