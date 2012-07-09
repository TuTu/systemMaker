#!/bin/bash
# $1 = input single molecule gro file
# $2 = number of grid points
# $3 = grid size in AA

if [ $# -lt 3 ]; then
  echo "Usage: $0 <single.gro> <num_grid_points> <grid distance in AA>"
  exit 1;
fi

python3.2 makeMol.py -i $1 -o tmp.gro -n $2
editconf_d -f tmp.gro -o ini.gro 

python3.2 makeDest.py dest.xyz $2 -d $3

vmd -dispdev text -e arrange.tcl 

