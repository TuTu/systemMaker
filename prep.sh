#!/bin/bash

python3.2 makeMol.py -i dmu3_single.gro -o ini.gro -n $1
editconf_d -f ini.gro -o ini.gro 

python3.2 makeDest.py dest.xyz $1 -d $2

vmd -dispdev text -e arrange.tcl 

