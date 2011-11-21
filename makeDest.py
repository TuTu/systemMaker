import argparse
import math
import itertools

parser = argparse.ArgumentParser(description='Create 3D grid points')
parser.add_argument('outFile', nargs=1, type=argparse.FileType('w'),
    help='output file')
parser.add_argument('numPoints', nargs=1, type=int,
    help='number of points')
parser.add_argument('-d', '--pointDistance', nargs=1, type=float, required=True,
    help='distance between points')

args = parser.parse_args()
outFile = args.outFile[0]
numPoints = args.numPoints[0]
pointDistance = args.pointDistance[0]

#maxDimemsion = int(math.ceil((numPoints)**(1.0/3.0)))
cubicDimension = int(math.floor((numPoints)**(1.0/3.0)))
numPointsLeft = numPoints - (cubicDimension)**3
  #the dimension of the cube which can be constructed completely by the given number of points
  #here the "dimension" is actually the number of grid points of the cubic length
  #the origin is on a corner of the cube

#numPoints=1 -> maxDimension=1 (coordinate iterate from 0 to 0)
#          1-7 -> cubicDimension=0
#numPoints=2-8 -> maxDimension=2 (coordinate iterate from 0 to 1)
#          8-26 -> cubicDimension=1
#numPoints=9-27 -> maxDimension=3 (coordinate iterate from 0 to 2)
#          27-63 -> cubicDimension=2

def permute(vec):
    perm = itertools.permutations(vec)
    return list(set([i for i in perm])) #remove duplicate permutations

#def getShell(layer)
#    prod = [i for i in itertools.product([layer],[0,layer],[0,layer])]
#    perm = [itertools.permutations(j) for j in prod]
#    for i in range(0, len(perm)):
#        shellPoints += [j for j in perm[i]]
#    return list(set(shellPoints)) #remove duplicate terms

def getShell(layer):
    prod = [i for i in itertools.product([layer-1], range(0, layer), range(0, layer))]
    shellPoints = []
    for i in prod:
        shellPoints += permute(i)
    return list(set(shellPoints)) #remove duplicate terms

def getCubic(dim):
    prod = [i for i in itertools.product(range(0, dim), range(0, dim), range(0, dim))]
    cubicPoints = []
    for i in prod:
        cubicPoints += permute(i)
    return list(set(cubicPoints)) #remove duplicate terms

#construct pointStack as a warehouse of points
#def stackByDistance(stack, dim, num):
#    distPointList = {}
#    count = 0
#    for i in range(0, dim):
#        for j in range(0, dim):
#            for k in range(0, dim):
#                distPointList.setdefault(i*i + j*j + k*k, []).append([i, j, k])
#    for i in sorted(distPointList):
#        for point in distPointList[i]:
#            stack.append(point)
#    return stack

#def outputStack(stack, num, output):
#    count = 0
#    for i in sorted(pointStack):
#        for point in pointStack[i]:
#            outFile.write("%f %f %f" % tuple([p * pointDistance for p in point]) + '\n')
#            count += 1
#            if count == num:
#                return


points = getCubic(cubicDimension) + getShell(cubicDimension + 1)[0:numPointsLeft]

#output
outFile.write(str(numPoints) + '\n')
for point in points:
    outFile.write("%f %f %f" % tuple([i * pointDistance for i in point]) + '\n')

#stacking(pointStack, numPoints, outFile)
outFile.close()

