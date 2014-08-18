import argparse
import math
import itertools

parser = argparse.ArgumentParser(description='Create 3D grid points')
parser.add_argument('numPoints', type=int,
    help='number of points')
parser.add_argument('-o', '--outFile', type=argparse.FileType('w'), required=True,
    help='output file')
parser.add_argument('-d', '--pointDistance', type=float, required=True,
    help='distance between points in Angstrom')
parser.add_argument('--offset', type=float, default=0.,
    help='offset of all coordinates in Angstrom, dx dy dz')
parser.add_argument('-t', '--type', default='cubic',
    help='point-stack geometry: cubic (default) or pillar')

args = parser.parse_args()
outFile = args.outFile
numPoints = args.numPoints
pointDistance = args.pointDistance
type = args.type

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
    pass


if type == 'cubic':
    cubicDimension = int(math.floor((numPoints)**(1.0/3.0)))
    numPointsLeft = numPoints - (cubicDimension)**3
  #the dimension of the cube which can be constructed completely by the given number of points
  #here the "dimension" is actually the number of grid points of the cubic length
  #the origin is on a corner of the cube

    points = getCubic(cubicDimension) + getShell(cubicDimension + 1)[0:numPointsLeft]

elif type == 'pillar':
    pass
    

#output
outFile.write(str(numPoints) + '\n')
for point in points:
    outFile.write("%f %f %f" % tuple([p * pointDistance + args.offset for p in point]) + '\n')

#stacking(pointStack, numPoints, outFile)
outFile.close()

