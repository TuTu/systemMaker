source ~/osmolyte_ffmixed/tools/systemMaker/mol_man.tcl

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

foreach sel $sel_list {
    puts [geom_center $sel]
}

puts "------------"

foreach sel $sel_list position $position_list {
    mol_rand_rot $sel
    mol_move $sel $position
}

puts "------------"

foreach sel $sel_list {
    puts [geom_center $sel]
}

[atomselect top "all"] writepdb new.pdb
exit
