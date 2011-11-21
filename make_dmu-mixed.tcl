source mol_man.tcl
set num_cc 6
set num_ct 2
set num_tot [expr $num_cc + $num_ct]

set dist 4
set dest_list [list \
          [list -$dist -$dist $dist] [list $dist $dist -$dist] \
          [list $dist -$dist $dist] [list $dist -$dist -$dist] \
          [list -$dist $dist $dist] [list -$dist $dist -$dist] \
          [list $dist $dist $dist] [list -$dist -$dist -$dist]]

set ini_gro dmu_mixed_unit.gro
mol new $ini_gro

for {set i 1} {$i <= $num_tot} {incr i} {
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
