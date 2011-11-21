#!/bin/bash

python3.2 duplicateMol.py dmu3_single.gro ini.gro $1
editconf_d -f ini.gro -o ini.gro 

python3.2 makeDest.py dest.xyz $1 -d $2

vmd -dispdev text -e make.tcl 

