#!/bin/bash
# $1 = input single molecule gro file
# $2 = number of grid points
# $3 = grid size in AA

if [ $# -lt 3 ]; then
  echo "Usage: $0 <single.gro> <num_grid_points> <grid distance in AA>"
  exit 1;
fi

#duplicate single molecules to multiple molecules in tmp.gro
python3.2 makeMol.py -i $1 -o tmp.gro -n $2 &&

#adjust the format (number sequence), make it a legal gro file
editconf_d -f tmp.gro -o ini.gro &&

#generate desired grids
python3.2 makePoints.py $2 -o grid.xyz -d $3 &&

#arrange the molecules on the grids
vmd -dispdev text -e arrange.tcl -args ini.gro grid.xyz 

