*templatefileset "D:/Program_Files/Altair/2019/templates/feoutput/optistruct/optistruct"
*readfile "E:/User/DC/bending-optimization/modeling/VT-bending-CT layer element.hm"

*start_batch_import 1
*mergefile2  filename="E:\\User\\DC\\bending-optimization\\modeling\\VT-bending-PD element.hm" mergemode.props=keepboth mergemode.mats=keepboth mergemode.comps=keepboth mergemode.geometryandmesh=keepboth mergemode.modules=keepexisting mergemode.connectors=keepincoming connectors.tolerancecheck=true connectors.tolerance=0.1 connectors.idcheck=true connectors.thicknesscheck=true connectors.layercheck=true connectors.type=true connectors.checkattribute=false
*setgeomrefinelevel 1
*end_batch_import 

*createmark components 1 "all"
set comp_lst [hm_getmark comps 1]
set PD_list [list]
set layer_list [list]
set PDid_list [list]
set layerid_list [list]
set resin_list [list]
set resinid_list [list]
set str1 "PD"
set str2 "layer"
set name "layer-"

foreach comp_id $comp_lst {
	set comp_name [hm_getvalue comps id=$comp_id dataname=name]
	set name_deter1 [string range $comp_name 0 1]
	set name_deter2 [string range $comp_name 0 4]
	if {[string equal $name_deter1 $str1] eq 1} {
		lappend PD_list $comp_name
		lappend PDid_list $comp_id
	} elseif {[string equal $name_deter2 $str2] eq 1} {
		lappend layer_list $comp_name
		lappend layerid_list $comp_id
	} else {
		lappend resin_list $comp_name
		lappend resinid_list $comp_id
	}
}


#Reclassify and integrate element numbers based on component name search
foreach ply_drop2 $PD_list {
	if {[string length $ply_drop2] eq 7} {
		set final_num [string index $ply_drop2 end]
		set ply_elements_id [hm_getvalue comps name=$ply_drop2 dataname=elements]
		if {[llength $ply_elements_id] eq 0} {
			*startnotehistorystate {Deleted Component $ply_drop2}
			*createmark components 1 $ply_drop2
			*deletemark components 1
			*endnotehistorystate {Deleted Component $ply_drop2}
		} else {
			foreach ply_elements $ply_elements_id {
				*createmark elements 1 $ply_elements
				*movemark elements 1 "$name$final_num"
			}
			*startnotehistorystate {Deleted Component $ply_drop2}
			*createmark components 1 $ply_drop2
			*deletemark components 1
			*endnotehistorystate {Deleted Component $ply_drop2}
		}
	} elseif {[string length $ply_drop2] eq 8} {
		set final_num [string range $ply_drop2 end-1 end]
		set ply_elements_id [hm_getvalue comps name=$ply_drop2 dataname=elements]
		if {[llength $ply_elements_id] eq 0} {
			*startnotehistorystate {Deleted Component $ply_drop2}
			*createmark components 1 $ply_drop2
			*deletemark components 1
			*endnotehistorystate {Deleted Component $ply_drop2}
		} else {
			foreach ply_elements $ply_elements_id {
				*createmark elements 1 $ply_elements
				*movemark elements 1 "$name$final_num"
			}
			*startnotehistorystate {Deleted Component $ply_drop2}
			*createmark components 1 $ply_drop2
			*deletemark components 1
			*endnotehistorystate {Deleted Component $ply_drop2}
		}
	}
}

*createstringarray 11 "OptiStruct " " " "ANSA " "PATRAN " "EXPAND_IDS_FOR_FORMULA_SETS " \
  "ASSIGNPROP_BYHMCOMMENTS" "LOADCOLS_DISPLAY_SKIP " "VECTORCOLS_DISPLAY_SKIP " \
  "SYSTCOLS_DISPLAY_SKIP " "CONTACTSURF_DISPLAY_SKIP " "IMPORT_MATERIAL_METADATA"
*feinputwithdata2 "\#optistruct\\optistruct" "E:/User/DC/bending-optimization/modeling/reinforce-piece.fem" 0 0 0 0 0 1 11 1 0

*startnotehistorystate {Modified Property of component from 0 to 1}
*setvalue comps id=34 propertyid={props 1}
*endnotehistorystate {Modified Property of component from 0 to 1}
*startnotehistorystate {Updated "propertyid" of Components}
*createmark components 1 "Reinforce-piece"
*clearmark components 1
*endnotehistorystate {Updated "propertyid" of Components}

*createstringarray 11 "OptiStruct " " " "ANSA " "PATRAN " "EXPAND_IDS_FOR_FORMULA_SETS " \
  "ASSIGNPROP_BYHMCOMMENTS" "LOADCOLS_DISPLAY_SKIP " "VECTORCOLS_DISPLAY_SKIP " \
  "SYSTCOLS_DISPLAY_SKIP " "CONTACTSURF_DISPLAY_SKIP " "IMPORT_MATERIAL_METADATA"
*feinputwithdata2 "\#optistruct\\optistruct" "E:/User/DC/bending-optimization/modeling/bend-clamp.fem" 0 0 0 0 0 1 11 1 0


*templatefileset "D:/Program_Files/Altair/2019/templates/feoutput/abaqus/standard.3d"
*createentity props cardimage=SHELLSECTION includeid=0 name=property1
*createmark properties 1 "property1"
*clearmark properties 1
#Giving materials properties to the reestablish elements which in order to establish the sets when importing the ABAQUS
*createmark components 1 "all"
set comp_lst [hm_getmark comps 1]
foreach comp_id $comp_lst {
	set comp_name [hm_getvalue comps id=$comp_id dataname=name]
	*startnotehistorystate {Modified Property of component}
	*setvalue comps mark=1 propertyid={props 1}
	*endnotehistorystate {Modified Property of component}
	*startnotehistorystate {Updated "propertyid" of Components}
	*createmark components 1 $comp_name
	*clearmark components 1
	*endnotehistorystate {Updated "propertyid" of Components}
}


*createmark elements 1 "displayed"
*equivalence elements 1 0.0001 1 0 0

hm_answernext yes
*writefile "E:/User/DC/bending-optimization/modeling/pretreatment-model.hm" 1

*createstringarray 4 "HMBOMCOMMENTS_XML" "HMMATCOMMENTS_XML" "EXPORTIDS_SKIP" "IDRULES_SKIP"
hm_answernext yes
*feoutputwithdata "D:/Program_Files/Altair/2019/templates/feoutput/abaqus/standard.3d" "E:/User/DC/bending-optimization/modeling/pretreatment-model.inp" 0 0 1 1 4