import argparse
import sys

#inFile = open(inFilename, 'r')
#outFile = open(outFilename, 'w')

parser = argparse.ArgumentParser(description='Duplicate and stack molecules into a single gro file')
parser.add_argument('-i', '--inFile', nargs='+', type=argparse.FileType('r'), required=True,
    help='Gromacs gro files, containing molecules to be duplicated in sequence.')
parser.add_argument('-o', '--outFile', nargs=1, type=argparse.FileType('w'), required=True,
    help='Gromacs gro file.')
parser.add_argument('-n', '--numDup', nargs='+', type=int, required=True,
    help='Number of duplication (including the original one) for each molecule type in sequence.')

args = parser.parse_args()
inFileList = args.inFile
outFile = args.outFile[0]
numDup = args.numDup

if len(inFileList) != len(numDup):
    sys.exit("ERROR: The numbers of --inFile and --numDup arguments should be consistent.")


outFile.write("Built from:" + str([f.name for f in inFileList]) + '\n')
numAtom = []

#get number of atoms of each file (read only the first two lines)
for inFile in inFileList:
    for (i, line) in enumerate(inFile):
        if i == 1:
            numAtom.append(int(line.split()[0]))
            break

totNumAtom = sum([numAtom[i]*numDup[i] for i in range(0, len(numDup))])
outFile.write(str(totNumAtom) + '\n')

resCount = 0
for (inFileIndex, inFile) in enumerate(inFileList):
    molLines = []
    for (i, line) in enumerate(inFile):
        if i < numAtom[inFileIndex] :
            molLines.append(line[5:])

    for i in range(1,numDup[inFileIndex]+1):
        resCount += 1
        for line in molLines:
            outFile.write("%5d%s" % (resCount, line))
    inFile.close()

outFile.close()
