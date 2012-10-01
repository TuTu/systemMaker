#This script arranges molecules radially outward from the origin
#with specified positions

if { $argc != 3 } {
    puts "Usage: -args <molecules.gro> <positions.xyz>"
    exit 1
} else {
    set ini_gro [lindex $argv 0]
    set position_filename [lindex $argv 1]
}

puts "Please make sure the first line of $position_filename\
is the total number of the following lines, i.e. the total number of positions."


set position_file [open $position_filename r]
set position_data [read $position_file]
close $position_file
set position_data [split $position_data \n]

set num_mol [lindex $position_data 0]
set position_list [lrange $position_data 1 $num_mol]

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
    return [list $r [expr {acos($z/$r)}] [expr {atan2($y, $x)}]]
}

proc rot_sphere {sphe} {
    return [trans axis y [lindex $sphe 1] rad \
                  axis z [lindex $sphe 2] rad]
}

foreach sel $sel_list position $position_list {
    set rand_rot [trans axis z [expr rand()*360] deg]
    $sel move $rand_rot
    $sel move [rot_sphere [cart2sphe $position]]
    $sel moveby $position
}

[atomselect top "all"] writepdb new.pdb
put end
exit
