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
parser.add_argument('-t', '--type', nargs=1, required=True,
    help='point-stack geometry: cubic, pillar')

args = parser.parse_args()
outFile = args.outFile[0]
numPoints = args.numPoints[0]
pointDistance = args.pointDistance[0]
type = args.type[0]

def permute(vec):
    perm = itertools.permutations(vec)
    return list(set([i for i in perm])) #remove duplicate permutations

def getShell(layer):
    prod = [i for i in itertools.product([layer-1], range(0, layer), range(0, layer))]
    shellPoints = []
    for i in prod:
        shellPoints += permute(i)
    return list(set(shellPoints)) #remove duplicate terms

def getCubic(dim):
    prod = [i for i in itertools.product(range(0, dim), range(0, dim), range(0, dim))]
#    cubicPoints = []
#    for i in prod:
#        cubicPoints += permute(i)
#    return list(set(cubicPoints)) #remove duplicate terms
    return prod

def getPillar(bottom, height):


if type == 'cubic':
    cubicDimension = int(math.floor((numPoints)**(1.0/3.0)))
    numPointsLeft = numPoints - (cubicDimension)**3
  #the dimension of the cube which can be constructed completely by the given number of points
  #here the "dimension" is actually the number of grid points of the cubic length
  #the origin is on a corner of the cube

    points = getCubic(cubicDimension) + getShell(cubicDimension + 1)[0:numPointsLeft]

elif type == 'pillar':
    

#output
outFile.write(str(numPoints) + '\n')
for point in points:
    outFile.write("%f %f %f" % tuple([i * pointDistance for i in point]) + '\n')

#stacking(pointStack, numPoints, outFile)
outFile.close()

