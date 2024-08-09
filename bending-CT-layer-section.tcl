*templatefileset "D:/Program_Files/Altair/2019/templates/feoutput/optistruct/optistruct"
*readfile "E:/User/DC/bending-optimization/modeling/VT-bending-CT layer base element.hm"
set filepath {E:/User/DC/bending-optimization/modeling/ply-drop-sequence1.txt}
set chan [open $filepath r] 
gets $chan line
#puts $line
close $chan
set SSTins_length [llength $line]
set name "layer-"

set PD_start_element_number 40000
set element_dengcha 1027

#Dividing units into belonging layers based on ply drop
for {set PD_num 1} {$PD_num <= $SSTins_length} {incr PD_num 1} {
	if {[lindex $line [expr {$PD_num-1}]] eq 0} {
		set PD_end_element_number [expr {$PD_start_element_number+$element_dengcha-1}]
		for {set elemet_index $PD_start_element_number} {$elemet_index <= $PD_end_element_number} {incr elemet_index 1} {
			*createmark elements 1 $elemet_index
			*movemark elements 1 "$name$PD_num"
		}
		set PD_start_element_number [expr {$PD_end_element_number+1}]
	}
}

#delet initial components
*startnotehistorystate {Deleted Component "base element"}
*createmark components 1 "base element"
*deletemark components 1
*endnotehistorystate {Deleted Component "base element"}

#save the model
hm_answernext yes
*writefile "E:/User/DC/bending-optimization/modeling/VT-bending-CT layer element.hm" 1

*retainmarkselections 0
*createstringarray 4 "HM_NODEELEMS_SET_COMPRESS_SKIP " "HMBOMCOMMENTS_XML" \
  "HMMATCOMMENTS_XML" "IDRULES_SKIP"
hm_answernext yes
*feoutputwithdata "D:/Program_Files/Altair/2019/templates/feoutput/abaqus/standard.3d" "E:/User/DC/bending-optimization/modeling/VT-bending-CT layer element.fem"