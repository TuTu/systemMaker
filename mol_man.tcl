
proc geom_center {selection} {
    # set the geometrical center to 0
    set gc [veczero]
    # [$selection get {x y z}] returns a list of {x y z}
    #   values (one per atoms) so get each term one by one
    foreach coord [$selection get {x y z}] {
        # sum up the coordinates
        set gc [vecadd $gc $coord]
    }
    # and scale by the inverse of the number of atoms
    return [vecscale [expr 1.0 /[$selection num]] $gc]
}


proc mol_move {selection destination} {
    set offset [vecsub $destination [geom_center $selection]]
    $selection moveby $offset
}


proc mol_rand_rot {selection} {
    set ang1 [expr rand()*360]
    set ang2 [expr rand()*360]
    set ang3 [expr rand()*360]
    set rot [trans center [geom_center $selection] \
             axis x $ang1 deg \
             axis y $ang2 deg \
             axis z $ang3 deg]
    $selection move $rot
}


