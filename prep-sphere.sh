#!/bin/bash
# $1 = input single molecule gro file
# $2 = number of points
# $3 = minimal distance allowed

if [ $# -lt 3 ]; then
  echo "Usage: $0 <single.gro> <num of points> <minimal distance allowed in AA>"
  exit 1;
fi

#duplicate single molecules to multiple molecules in tmp.gro
python3.2 makeMol.py -i $1 -o tmp.gro -n $2 &&

#adjust the format (number sequence), make it a legal gro file
editconf_d -f tmp.gro -o ini.gro &&

#generate random sphere points
python3.2 makeSpherePoints.py sphere.xyz $2 $3 &&

#arrange the molecules radially outward on the sphere points
vmd -dispdev text -e arrange-radial.tcl -args ini.gro sphere.xyz

