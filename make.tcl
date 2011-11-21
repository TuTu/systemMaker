source ~/osmolyte_ffmixed/tools/make_unit/mol_man.tcl

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

foreach sel $sel_list {
    puts [geom_center $sel]
}

puts "------------"

foreach sel $sel_list dest $dest_list {
    mol_rand_rot $sel
    mol_move $sel $dest
}

puts "------------"

foreach sel $sel_list {
    puts [geom_center $sel]
}

[atomselect top "all"] writepdb new.pdb
exit
