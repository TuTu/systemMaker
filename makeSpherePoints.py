import argparse
import math
import random
import sys

parser = argparse.ArgumentParser(description='Create 3D mesh points for sphere')
parser.add_argument('outFile', type=argparse.FileType('w'),
    help='output file')
parser.add_argument('numPoints', type=int,
    help='number of points')
parser.add_argument('minDistance', type=float,
    help='minimum distance between points')
parser.add_argument('-t', '--tryLimit', type=int, default=10000,
    help='try limit (default 10000)')
parser.add_argument('-i', '--interactive', action='store_true',
    help='interactive mode')

args = parser.parse_args()
outFile = args.outFile
numPoints = args.numPoints
minDistance = args.minDistance
tryLimit = args.tryLimit
isInteractive = args.interactive

currentMinDistSquare = -1
criteriaReduceRatio = 0.9

def setCriteria(criteria):
    global unitMinDistCriteria
    global unitMinDistCriteriaSquare
    unitMinDistCriteria = criteria
    unitMinDistCriteriaSquare = criteria**2
    print("unitMinDistCriteria = " + str(unitMinDistCriteria))

setCriteria(3 / math.sqrt(numPoints)) #Minimum distance for a unit shpere, 
                                  #this is just a rough value
                                  #n*pi*r^2 = 4*pi*1^2 --> D=2r=4/sqrt(n)
                                  #For safty, I choose a smaller value 3/sqrt(n)
                                  #otherwise, the shpere may not fit n points.

def getDistanceSquare(p1, p2):
    return sum([(p1i - p2i)**2 for (p1i, p2i) in zip(p1, p2)])

def isRejected(newPoint, points):
    global currentMinDistSquare
    global unitMinDistCriteriaSquare
    distSquareList = [-1] * len(points)
    for (i, p) in enumerate(points):
        distSquare = getDistanceSquare(newPoint, p) 
        if distSquare < unitMinDistCriteriaSquare:
            return True
        else:
            distSquareList[i] = distSquare
    minTemp = min(distSquareList)
    if minTemp < 0:
        sys.exit("Error: something is wrong in finding the minimum distance.\n"+
                 "       Number of pairs is inconsistent.")
    elif currentMinDistSquare < 0:
        currentMinDistSquare = minTemp
    else:
        if minTemp < currentMinDistSquare:
            currentMinDistSquare = minTemp
            print("currentMinDist: " + str(math.sqrt(currentMinDistSquare)))
    return False

def getNormalized(p):
    r = math.sqrt(sum([pi**2 for pi in p]))
    return [pi/r for pi in p]

def getNewPoint():
    while True:
        p = [random.random() for _ in range(3)]
        p = [pi*2 - 1 for pi in p]
        if getDistanceSquare(p, [0, 0, 0]) <= 1:
            break
    return getNormalized(p)

points = [[0, 0, 0] for _ in range(numPoints)]
points[0] = getNewPoint()

numTry = 1
index = 1
while index < numPoints:
    newPoint = getNewPoint()
    while isRejected(newPoint, points[:index]):
        numTry = numTry + 1
        if numTry > tryLimit:
            if isInteractive:
                print("Try limit " + str(tryLimit) + " is reached.\n" +
                      "Would you like to:\n" +
                      "a) try more times\n" +
                      "b) reduce the critera\n" +
                      "c) quit")
                while True:
                    tryMoreAns = input("(a/b/c): ")
                    if tryMoreAns == "a":
                        numTry = 0
                        break
                    elif tryMoreAns == "b":
                        numTry = 0
                        setCriteria(unitMinDistCriteria * criteriaReduceRatio)
                        break
                    elif tryMoreAns == "c":
                        numTry = -1
                        break
                    else:
                        continue
            else:
                numTry = 0
                setCriteria(unitMinDistCriteria * criteriaReduceRatio)
        else:
            newPoint = getNewPoint()
            continue
        break #tryMore

    if numTry > 0: #new point found! if numTry == 0, tryMore is carried out by user
        points[index] = newPoint
        index = index + 1
        print("We now have " + str(index) + " points in hand.")
    elif numTry < 0: #try no more, quit
        break
    numTry = 1

ratio = minDistance /  math.sqrt(currentMinDistSquare)
points = [[pi*ratio for pi in p] for p in points[:index]]

print("currentMinDist: " + str(math.sqrt(currentMinDistSquare)))
print("ratio (radius): " + str(ratio))

#output
outFile.write(str(index) + '\n')
for point in points:
    outFile.write("%f %f %f" % tuple(point) + '\n')

#stacking(pointStack, numPoints, outFile)
outFile.close()
