#return the minium distance between selected atoms
proc min_dist {sel} {
    set isFirst 1
    set i 1
    foreach coord1 [$sel get {x y z}] {
        set j 1
        foreach coord2 [$sel get {x y z}] {
            if {$j > $i} {
                set tmp [veclength [vecsub $coord1 $coord2]]           
                if {$isFirst == 1} {
                    set min $tmp
                    set isFirst 0
                } else {
                    if {$tmp < $min} {
                        set min $tmp
                    }
                }
            }
            incr j
        }
        incr i
    }
    return $min
}
