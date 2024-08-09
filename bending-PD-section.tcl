*templatefileset "D:/Program_Files/Altair/2019/templates/feoutput/optistruct/optistruct"
*readfile "E:/User/DC/bending-optimization/modeling/VT-bending-PD base element.hm"
set filepath {E:/User/DC/bending-optimization/modeling/ply-drop-sequence.txt}
set chan [open $filepath r] 
gets $chan line
close $chan
set SSTins_length [llength $line]
set name "PD-ply"

#creat components
*createentity comps includeid=0 name=Resin-pocket
*createmark components 1 "Resin-pocket"
*clearmark components 1
for {set plynum 1} {$plynum <= $SSTins_length} {incr plynum 1} {
	*createentity comps includeid=0 name=$name$plynum
	*createmark components 1 "$name$plynum"
	*clearmark components 1
}

set PD_start_node [list 1 15 29 43 57 71 85 99 113 127 141 155 169]
set PD_start_element [list 1 14 27 40 53 66 79 92 105 118 131 144]
set PD_start_element_number 1
set PD_end_element_number 144
set node_dengcha 14
set element_dengcha 13

proc Maxvalue {lst} {
	set res [lsort -integer $lst]
	set result [lindex $res end]
	return $result
}

#The use of 2D mesh drag operation is to generate layers with unidirectional normal always in the stacking direction
*startnotehistorystate {Component "base element" made current}
*currentcollector components "base element"
*endnotehistorystate {Component "base element" made current}
for {set PD_num 1} {$PD_num <= $SSTins_length} {incr PD_num 1} {
	set PD_start_node_length [llength $PD_start_node]
	set PD_start_element_length [llength $PD_start_element]
	
	set PD_start_node_max [Maxvalue $PD_start_node]
	set PD_start_node_nextply [list]

	set PD_start_element_max [Maxvalue $PD_start_element]
	set PD_start_element_nextply [list]
	if {[lindex $line [expr {$PD_num-1}]] eq 0} {
		#If no ply drop occurs, all nodes and surface elements will be shifted upwards by one thickness
		for {set start_node_index 1} {$start_node_index <= $PD_start_node_length} {incr start_node_index 1} {
			set initial_PD_start_node [lindex $PD_start_node [expr {$start_node_index-1}]]
			set next_PD_start_node [expr {$PD_start_node_max + $start_node_index*$node_dengcha}]
			for {set node_transverse 1} {$node_transverse <= $node_dengcha} {incr node_transverse 1} {
				*createmark nodes 1 [expr {$initial_PD_start_node + $node_transverse-1}]
				*duplicatemark nodes 1 28
				*createmark nodes 1 [expr {$next_PD_start_node + $node_transverse-1}]
				*createvector 1 0 0 1
				*translatemark nodes 1 1 0.2
			}
			lappend PD_start_node_nextply $next_PD_start_node
		}
		
		#Based on node number information, generate the surface bottom layer elements for the next layer and update the element number information list
		for {set start_element_index 1} {$start_element_index <= $PD_start_element_length} {incr start_element_index 1} {
			set next_PD_start_element [expr {$PD_start_element_max+$start_element_index*$element_dengcha}]
			lappend PD_start_element_nextply $next_PD_start_element 
		}
		for {set start_node_index 1} {$start_node_index < $PD_start_node_length} {incr start_node_index 1} {
			set face_element_node_start1 [lindex $PD_start_node_nextply [expr {$start_node_index-1}]]
			set face_element_node_start2 [lindex $PD_start_node_nextply $start_node_index]
			for {set node_transverse 1} {$node_transverse < $node_dengcha} {incr node_transverse 1} {
				*createlist nodes 1 [expr {$face_element_node_start1+$node_transverse-1}] [expr {$face_element_node_start1+$node_transverse}] [expr {$face_element_node_start2+$node_transverse-1}] [expr {$face_element_node_start2+$node_transverse}]
				*createelement 104 1 1 1
			}
		}
		
	} else {
		#ply drop occurs。
		set PD_number [lindex $line [expr {$PD_num-1}]]
		for {set start_node_index 1} {$start_node_index <= $PD_number} {incr start_node_index 1} {
			set initial_PD_start_node [lindex $PD_start_node [expr {$start_node_index-1}]]
			set next_PD_start_node [expr {$PD_start_node_max + $start_node_index*$node_dengcha}]
			for {set node_transverse 1} {$node_transverse <= $node_dengcha} {incr node_transverse 1} {
				*createmark nodes 1 [expr {$initial_PD_start_node + $node_transverse-1}]
				*duplicatemark nodes 1 28
				*createmark nodes 1 [expr {$next_PD_start_node + $node_transverse-1}]
				*createvector 1 0 0 1
				*translatemark nodes 1 1 0.2
			}
			lappend PD_start_node_nextply $next_PD_start_node
		}
		set PD_start_node_add [lrange $PD_start_node $PD_number end]
		set PD_start_node_nextply [concat $PD_start_node_nextply $PD_start_node_add]
	
		
		#For layer occurs ply drops, first generate resin elements, and finally generate bottom surface elementss based on the node information above
		set resin_node_start1 [lindex $PD_start_node [expr {$PD_number-1}]]
		set resin_node_start2 [lindex $PD_start_node [expr {$PD_number}]]
		set resin_node_start3 [lindex $PD_start_node_nextply [expr {$PD_number-1}]]
		set resin_element_startelement [expr {$PD_start_element_max + $element_dengcha}]
		for {set element_transverse 1} {$element_transverse <= $element_dengcha} {incr element_transverse 1} {
			*createlist nodes 1 [expr {$resin_node_start1+$element_transverse-1}] [expr {$resin_node_start1+$element_transverse}] [expr {$resin_node_start2+$element_transverse-1}] [expr {$resin_node_start2+$element_transverse}] [expr {$resin_node_start3+$element_transverse-1}] [expr {$resin_node_start3+$element_transverse}]
			*createelement 206 1 1 1
			set each_resin_element [expr {$resin_element_startelement+$element_transverse-1}]
			*createmark elements 1 $each_resin_element
			*movemark elements 1 "Resin-pocket"
		}
		
		for {set start_element_index 1} {$start_element_index <= $PD_number} {incr start_element_index 1} {
			set next_PD_start_element [expr {$resin_element_startelement + $start_element_index*$element_dengcha}] 
			lappend PD_start_element_nextply $next_PD_start_element
		}
		for {set start_node_index 1} {$start_node_index <= $PD_number} {incr start_node_index 1} {
			set face_element_node_start1 [lindex $PD_start_node_nextply [expr {$start_node_index-1}]]
			set face_element_node_start2 [lindex $PD_start_node_nextply $start_node_index]
			for {set node_transverse 1} {$node_transverse < $node_dengcha} {incr node_transverse 1} {
				*createlist nodes 1 [expr {$face_element_node_start1+$node_transverse-1}] [expr {$face_element_node_start1+$node_transverse}] [expr {$face_element_node_start2+$node_transverse-1}] [expr {$face_element_node_start2+$node_transverse}]
				*createelement 104 1 1 1
			}
		}
		set PD_start_element_add [lrange $PD_start_element $PD_number end]
		set PD_start_element_nextply [concat $PD_start_element_nextply $PD_start_element_add]
	}
	#Update the starting node and element list information
	set PD_start_node $PD_start_node_nextply
	set PD_start_element $PD_start_element_nextply
}

#No ply drop occurrs, perform equal thickness elements 2D drag operation
set ply_element_index [expr {[lindex $PD_start_element end]+$element_dengcha-1}]
set PD_start_element [list 1 14 27 40 53 66 79 92 105 118 131 144]
for {set PD_num 1} {$PD_num <= $SSTins_length} {incr PD_num 1} {
	set index 1
	set PD_start_element_max [Maxvalue $PD_start_element]
	set PD_number [lindex $line [expr {$PD_num-1}]]
	set PD_start_element_nextply [list]
	if {$PD_number eq 0} {
		for {set start_element_index 1} {$start_element_index <= $PD_start_element_length} {incr start_element_index 1} {
			set initial_PD_start_element [lindex $PD_start_element [expr {$start_element_index-1}]]
			set next_PD_start_element [expr {$PD_start_element_max + $start_element_index*$element_dengcha}]
			for {set element_transverse 1} {$element_transverse <= $element_dengcha} {incr element_transverse 1} {
				*createmark elements 1 [expr {$initial_PD_start_element+$element_transverse-1}]
				*createvector 1 0 0 1
				*meshdragelements2 1 1 0.2 1 0 0 0
				set ply_element_index [expr {$ply_element_index+$index}]
				*createmark elements 1 $ply_element_index
				*movemark elements 1 "$name$PD_num"
			}
			lappend PD_start_element_nextply $next_PD_start_element
		}	
	} else {
		if {$PD_number ne 1} {
			for {set start_element_index 1} {$start_element_index < $PD_number} {incr start_element_index 1} {
				set initial_PD_start_element [lindex $PD_start_element [expr {$start_element_index-1}]]
				set next_PD_start_element [expr {$PD_start_element_max + ($start_element_index+1)*$element_dengcha}]
				for {set element_transverse 1} {$element_transverse <= $element_dengcha} {incr element_transverse 1} {
					*createmark elements 1 [expr {$initial_PD_start_element+$element_transverse-1}]
					*createvector 1 0 0 1
					*meshdragelements2 1 1 0.2 1 0 0 0
					set ply_element_index [expr {$ply_element_index+$index}]
					*createmark elements 1 $ply_element_index
					*movemark elements 1 "$name$PD_num"
				}
				lappend PD_start_element_nextply $next_PD_start_element
			}
			lappend PD_start_element_nextply [expr {$next_PD_start_element+$element_dengcha}]
			set PD_start_element_add [lrange $PD_start_element $PD_number end]
			set PD_start_element_nextply [concat $PD_start_element_nextply $PD_start_element_add]
		} else {
			set next_PD_start_element [expr {$PD_start_element_max + 2*$element_dengcha}]
			lappend PD_start_element_nextply $next_PD_start_element
			set PD_start_element_add [lrange $PD_start_element 1 end]
			set PD_start_element_nextply [concat $PD_start_element_nextply $PD_start_element_add]
		}
	}
	set PD_start_element $PD_start_element_nextply
}

*startnotehistorystate {Deleted Component "base element"}
*createmark components 1 "base element"
*deletemark components 1
*endnotehistorystate {Deleted Component "base element"}

#Perform a common node for all units
*createmark elements 1 "displayed"
*equivalence elements 1 0.01 1 0 0

hm_answernext yes
*writefile "E:/User/DC/bending-optimization/modeling/VT-bending-PD element.hm" 1

*retainmarkselections 0
*createstringarray 4 "HM_NODEELEMS_SET_COMPRESS_SKIP " "HMBOMCOMMENTS_XML" \
  "HMMATCOMMENTS_XML" "IDRULES_SKIP"
hm_answernext yes
*feoutputwithdata "D:/Program_Files/Altair/2019/templates/feoutput/abaqus/standard.3d" "E:/User/DC/bending-optimization/modeling/VT-bending-PD element.fem"