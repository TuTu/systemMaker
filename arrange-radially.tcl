source ~/osmolyte_ffmixed/tools/systemMaker/mol_man.tcl

set dest_filename "dest.xyz"
set ini_gro "ini.gro"

puts "Please make sure the first line of $dest_filename\
is the total number of the following lines, i.e. the total number of positions."


set dest_file [open $dest_filename r]
set dest_data [read $dest_file]
close $dest_file
set dest_data [split $dest_data \n]

set num_mol [lindex $dest_data 0]
set dest_list [lrange $dest_data 1 $num_mol]

#set dist 4
#set dest_list [list \
          [list -$dist -$dist $dist] [list $dist $dist -$dist] \
          [list $dist -$dist $dist] [list $dist -$dist -$dist] \
          [list -$dist $dist $dist] [list -$dist $dist -$dist] \
          [list $dist $dist $dist] [list -$dist -$dist -$dist]]

mol new $ini_gro

for {set i 1} {$i <= $num_mol} {incr i} {
    lappend sel_list [atomselect top "resid $i"] 
}

proc rand_rot {selection} {
    set ang [expr rand()*360]
    set rot [trans center [geom_center $selection] \
             axis x $ang1 deg \
             axis y $ang2 deg \
             axis z $ang3 deg]
    $selection move $rot
}

proc cart2sphe {cart} {
    set x [lindex $cart 0]
    set y [lindex $cart 1]
    set z [lindex $cart 2]
    set r [expr {sqrt($x*$x + $y*$y + $z*$z)}]
    return [list $r [expr {acos($z/$r)}] [expr {atan($y/$x)}]]
}

proc rot_sphere {sphe} {
    return [trans axis y [lindex $sphe 1] rad \
                  axis z [lindex $sphe 2] rad]
}

put A
foreach sel $sel_list dest $dest_list {
    set rand_rot [trans axis z [expr rand()*360] deg]
    $sel move $rand_rot
put B
    $sel move [rot_sphere [cart2sphe $dest]]
put C
    $sel moveby $dest
}

[atomselect top "all"] writepdb new.pdb
put end
exit
