#!/bin/bash
# $1 = number of grid points, $2 = grid size in AA

python3.2 makeMol.py -i ini.gro -o tmp.gro -n $1
editconf_d -f tmp.gro -o ini.gro 

python3.2 makeDest.py dest.xyz $1 -d $2

vmd -dispdev text -e arrange.tcl 

