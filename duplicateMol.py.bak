import argparse

#inFile = open(inFilename, 'r')
#outFile = open(outFilename, 'w')

parser = argparse.ArgumentParser(description='Duplicate molecules')
parser.add_argument('inFile', nargs=1, type=argparse.FileType('r'), 
    help='Gromacs gro file.')
parser.add_argument('outFile', nargs=1, type=argparse.FileType('w'),
    help='Gromacs gro file.')
parser.add_argument('num_dup', nargs=1, type=int,
    help='Number of duplication (including the original one).')

args = parser.parse_args()
inFile = args.inFile[0]
outFile = args.outFile[0]
num_dup = args.num_dup[0]

mol_lines = []

end_line = ""
for (i, line) in enumerate(inFile):
    if i == 0:
        outFile.write(line)
    elif i == 1:
        num_atom = int(line.split()[0])
        outFile.write(str(num_atom * num_dup) + '\n')
    elif i >= 2 and i < 2 + num_atom:
        mol_lines.append(line[5:])
    else:
        end_line = line

for n in range(1,num_dup+1):
    for (i, line) in enumerate(mol_lines):
        outFile.write("%5d%s" % (n, line))

outFile.write(end_line)

inFile.close()
outFile.close()
