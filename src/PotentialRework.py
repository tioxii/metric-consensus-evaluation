import itertools
import math

from numpy import mean
import ImportCSVData as dt

def calcDistanceEuclidean2D(firstPoint : tuple, secondPoint : tuple) -> float:
    firstCoord : float = firstPoint[0] - secondPoint[0]
    secondCoord : float = firstPoint[1] - secondPoint[1]
    return math.sqrt(pow(firstCoord, 2) + pow(secondCoord, 2))

def findIndex(point : tuple, opinions : list[tuple]) -> int:
    for opinion in opinions:
        if point == opinion[0]:
            return opinions.index(opinion)

def caluclateScoreForNode(index : int, nodes : list, opinions : list[tuple]):
    neighbors = nodes[:]
    node = nodes[index]
    del neighbors[index]
    subsets : list[tuple] = itertools.combinations(neighbors, 2)
    
    for subset in subsets:
        if(calcDistanceEuclidean2D(node, subset[0]) < calcDistanceEuclidean2D(node, subset[1])):
            myIndex : int = findIndex(subset[0], opinions)
            opinions[myIndex] = (opinions[myIndex][0], opinions[myIndex][1] + 1)
        else:
            myIndex : int = findIndex(subset[1], opinions)
            opinions[myIndex] = (opinions[myIndex][0], opinions[myIndex][1] + 1)

def calculatePotential(points : list[tuple[float, float]]) -> float:
    opinions = sorted(set(points))
    opinions = list(map(lambda x: (x, 0), opinions))

    for i in range(len(points)):
        caluclateScoreForNode(i, points, opinions)

    scores : list = list(map(lambda x: x[1], opinions))
    return 1 - ((max(scores) - 4851)/ (485100 -  4851))

def getPotential(path : str, round : int = 0) -> float:  
    data = dt.getData(path)
    rounds = dt.getElmentsAtIndex(data, 0)
    rounds = dt.getRounds(rounds)

    xval = dt.getXByRound(rounds[round], data)
    yval = dt.getYByRound(rounds[round], data)
    points = list(zip(xval,yval))
    
    return calculatePotential(points)

def main():
    path = 'results/potentialSpecific/positions/Random Clusters_R-100_SYNC-true_POSITIONS.csv'
    potential = getPotential(path, 0)
    print(potential)

if __name__ == '__main__':
    main()