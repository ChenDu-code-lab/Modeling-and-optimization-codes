#-*-coding:UTF-8-*-
from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup
import os
import sys
executeOnCaeStartup()
os.chdir(r"E:\User\DC\bending-optimization\abaqus-analysis")
session.journalOptions.setValues(replayGeometry=COORDINATE,recoverGeometry= COORDINATE)

#Import stacking sequence txt.file
f = open('E:/User/DC/bending-optimization/abaqus-analysis/stacking-sequence.txt','r')
SQ = f.readline()
f.close()
SQ = SQ.split(",")  #Attention: SQ is a string

#Import stacking sequence txt.file
f = open('E:/User/DC/bending-optimization/modeling/ply-drop-sequence.txt','r')
PDL = f.readline()
f.close()
PDL = PDL.split(",")  #Attention: SQ is a string

#Import bending specimen and insert cohesive seams between laminas
mdb.ModelFromInputFile(name='pretreatment-model', inputFileName="E:/User/DC/bending-optimization/modeling/pretreatment-model.inp")
p = mdb.models['pretreatment-model'].parts['PART-1']
f = p.elements
ele_start1, ele_start2, ele_start3 = 156, 3510, 32266
ele_cohesive_start= 59378
PDL_length = len(PDL)-2
PDL_index_list = range(PDL_length)
for PDL_index in PDL_index_list:
    PDL_i = int(PDL[PDL_index])
    cohesive_Elements = "CohesiveSeam-" + str(int(PDL_index)+1) + "-Elements"
    cohesive_TopSurf = "CohesiveSeam-" + str(int(PDL_index)+1) + "-TopSurf"
    cohesive_BottomSurf = "CohesiveSeam-" + str(int(PDL_index)+1) + "-BottomSurf"
    if PDL_i == 0:
        ele_end1 = ele_start1 + 156
        ele_end2 = ele_start2 + 1027
        ele_end3 = ele_start3 + 1027
        face2Elements = f[int(ele_start1):int(ele_end1)]+f[int(ele_start2):int(ele_end2)]+f[int(ele_start3):int(ele_end3)]
        pickedElemFaces = regionToolset.Region(face2Elements=face2Elements)
        p.insertElements(elemFaces=pickedElemFaces)
        p = mdb.models['pretreatment-model'].parts['PART-1']
        e = p.elements
        ele_cohesive_end = ele_cohesive_start+2210
        elements = e[int(ele_cohesive_start):int(ele_cohesive_end)]
        p.Set(elements=elements, name=cohesive_Elements)
        p = mdb.models['pretreatment-model'].parts['PART-1']
        f = p.elements  
        face2Elements = f[int(ele_cohesive_start):int(ele_cohesive_end)]
        p.Surface(face2Elements=face2Elements, name=cohesive_TopSurf)
        p = mdb.models['pretreatment-model'].parts['PART-1']
        f = p.elements
        face1Elements = f[int(ele_cohesive_start):int(ele_cohesive_end)]
        p.Surface(face1Elements=face1Elements, name=cohesive_BottomSurf)
        #update variables values
        ele_start1 = ele_end1
        ele_start2 = ele_end2
        ele_start3 = ele_end3
        ele_cohesive_start = ele_cohesive_end
    elif PDL_i == 1:
        ele_end2 = ele_start2 + 1027
        face2Elements = f[int(ele_start2):int(ele_end2)]
        pickedElemFaces = regionToolset.Region(face2Elements=face2Elements)
        p.insertElements(elemFaces=pickedElemFaces)
        p = mdb.models['pretreatment-model'].parts['PART-1']
        e = p.elements
        ele_cohesive_end = ele_cohesive_start+1027
        elements = e[int(ele_cohesive_start):int(ele_cohesive_end)]
        p.Set(elements=elements, name=cohesive_Elements)
        p = mdb.models['pretreatment-model'].parts['PART-1']
        f = p.elements  
        face2Elements = f[int(ele_cohesive_start):int(ele_cohesive_end)]
        p.Surface(face2Elements=face2Elements, name=cohesive_TopSurf)
        p = mdb.models['pretreatment-model'].parts['PART-1']
        f = p.elements
        face1Elements = f[int(ele_cohesive_start):int(ele_cohesive_end)]
        p.Surface(face1Elements=face1Elements, name=cohesive_BottomSurf)
        #update variables values
        ele_start2 = ele_end2
        ele_cohesive_start = ele_cohesive_end
    else:
        ele_end1 = ele_start1 + 13*int(PDL_i-1)
        ele_end2 = ele_start2 + 1027
        face2Elements = f[int(ele_start1):int(ele_end1)]+f[int(ele_start2):int(ele_end2)]
        pickedElemFaces = regionToolset.Region(face2Elements=face2Elements)
        p.insertElements(elemFaces=pickedElemFaces)
        p = mdb.models['pretreatment-model'].parts['PART-1']
        e = p.elements
        ele_cohesive_end = ele_cohesive_start+ele_end1-ele_start1+1027
        elements = e[int(ele_cohesive_start):int(ele_cohesive_end)]
        p.Set(elements=elements, name=cohesive_Elements)
        p = mdb.models['pretreatment-model'].parts['PART-1']
        f = p.elements  
        face2Elements = f[int(ele_cohesive_start):int(ele_cohesive_end)]
        p.Surface(face2Elements=face2Elements, name=cohesive_TopSurf)
        p = mdb.models['pretreatment-model'].parts['PART-1']
        f = p.elements
        face1Elements = f[int(ele_cohesive_start):int(ele_cohesive_end)]
        p.Surface(face1Elements=face1Elements, name=cohesive_BottomSurf)
        #update variables values
        ele_start1 = ele_end1
        ele_start2 = ele_end2
        ele_cohesive_start = ele_cohesive_end
        
mdb.saveAs(pathName='E:/User/DC/bending-optimization/abaqus-analysis/bending-test-cohesive.cae')
mdb.save()
mdb.Job(name='bending-test-cohesive', model='pretreatment-model', description='', type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', scratch='', resultsFormat=ODB, parallelizationMethodExplicit=DOMAIN, 
    numDomains=48, activateLoadBalancing=False, multiprocessingMode=DEFAULT, numCpus=48, numGPUs=0)
mdb.jobs['bending-test-cohesive'].writeInput(consistencyChecking=OFF)
Mdb()
a = mdb.models['Model-1'].rootAssembly
mdb.ModelFromInputFile(name='bending-test-cohesive', inputFileName='E:/User/DC/bending-optimization/abaqus-analysis/bending-test-cohesive.inp')
mdb.saveAs(pathName='E:/User/DC/bending-optimization/abaqus-analysis/bending-test-cohesive.cae')

#Import bending specimen and assign material properties
#set reinforce-piece properties
mdb.models['bending-test-cohesive'].Material(name='reinforce-piece')
mdb.models['bending-test-cohesive'].materials['reinforce-piece'].Density(table=((1.2e-09, ), ))
mdb.models['bending-test-cohesive'].materials['reinforce-piece'].Elastic(table=((3340.0, 0.31), ))
#set clamp Q235 properties
mdb.models['bending-test-cohesive'].Material(name='Q235')
mdb.models['bending-test-cohesive'].materials['Q235'].Density(table=((7.85e-09, ), ))
mdb.models['bending-test-cohesive'].materials['Q235'].Elastic(table=((210000.0, 0.3), ))
#set resin pocket properties
mdb.models['bending-test-cohesive'].Material(name='resin')
mdb.models['bending-test-cohesive'].materials['resin'].Density(table=((1.2e-09, ), ))
mdb.models['bending-test-cohesive'].materials['resin'].Elastic(table=((3780.0, 0.38), ))
#set lamina properties
mdb.models['bending-test-cohesive'].Material(name='lamina')
mdb.models['bending-test-cohesive'].materials['lamina'].Density(table=((1.6e-09, ), ))
mdb.models['bending-test-cohesive'].materials['lamina'].Elastic(type=LAMINA, table=((165000.0, 7560.0, 0.185, 4450.0, 4450.0, 3430.0), ))
mdb.models['bending-test-cohesive'].materials['lamina'].HashinDamageInitiation(table=((1840.0, 1180.0, 23.0, 150.0, 68.3, 68.3), ))
mdb.models['bending-test-cohesive'].materials['lamina'].hashinDamageInitiation.DamageEvolution(type=ENERGY, table=((190.0, 78.0, 2, 2.7), ))
#set cohesive properties
mdb.models['bending-test-cohesive'].Material(name='cohesive')
mdb.models['bending-test-cohesive'].materials['cohesive'].Density(table=((1.48e-09, ), ))
mdb.models['bending-test-cohesive'].materials['cohesive'].Elastic(type=TRACTION, table=((3780.0, 1420.0, 1420.0), ))
mdb.models['bending-test-cohesive'].materials['cohesive'].QuadsDamageInitiation(table=((56.4, 84.6, 84.6), ))
mdb.models['bending-test-cohesive'].materials['cohesive'].quadsDamageInitiation.DamageEvolution(type=ENERGY, mixedModeBehavior=BK, power=1.45, table=((0.35, 0.98, 0.98), ))  
mdb.models['bending-test-cohesive'].materials['cohesive'].quadsDamageInitiation.DamageStabilizationCohesive(cohesiveCoeff=1e-05)

#create section
mdb.models['bending-test-cohesive'].HomogeneousSolidSection(name='reinforce-piece', material='reinforce-piece', thickness=None)
mdb.models['bending-test-cohesive'].HomogeneousSolidSection(name='Q235', material='Q235', thickness=None)
mdb.models['bending-test-cohesive'].HomogeneousSolidSection(name='resin', material='resin', thickness=None)

sectionLayer1 = section.SectionLayer(material='lamina', thickness=0.2, orientAngle=0.0, numIntPts=3, plyName='')
mdb.models['bending-test-cohesive'].CompositeShellSection(name='lamina-0D', preIntegrate=OFF, idealization=NO_IDEALIZATION, symmetric=False, thicknessType=UNIFORM, poissonDefinition=DEFAULT, thicknessModulus=None, 
    temperature=GRADIENT, useDensity=OFF, integrationRule=SIMPSON, layup=(sectionLayer1, ))

sectionLayer1 = section.SectionLayer(material='lamina', thickness=0.2, orientAngle=45.0, numIntPts=3, plyName='')
mdb.models['bending-test-cohesive'].CompositeShellSection(name='lamina-45D', preIntegrate=OFF, idealization=NO_IDEALIZATION, symmetric=False, thicknessType=UNIFORM, poissonDefinition=DEFAULT, thicknessModulus=None, 
    temperature=GRADIENT, useDensity=OFF, integrationRule=SIMPSON, layup=(sectionLayer1, ))

sectionLayer1 = section.SectionLayer(material='lamina', thickness=0.2, orientAngle=-45.0, numIntPts=3, plyName='')
mdb.models['bending-test-cohesive'].CompositeShellSection(name='lamina-N45D', preIntegrate=OFF, idealization=NO_IDEALIZATION, symmetric=False, thicknessType=UNIFORM, poissonDefinition=DEFAULT, thicknessModulus=None, 
    temperature=GRADIENT, useDensity=OFF, integrationRule=SIMPSON, layup=(sectionLayer1, ))
    
sectionLayer1 = section.SectionLayer(material='lamina', thickness=0.2, orientAngle=90.0, numIntPts=3, plyName='')
mdb.models['bending-test-cohesive'].CompositeShellSection(name='lamina-90D', preIntegrate=OFF, idealization=NO_IDEALIZATION, symmetric=False, thicknessType=UNIFORM, poissonDefinition=DEFAULT, thicknessModulus=None, 
    temperature=GRADIENT, useDensity=OFF, integrationRule=SIMPSON, layup=(sectionLayer1, ))    
    
mdb.models['bending-test-cohesive'].CohesiveSection(name='cohesive', material='cohesive', response=TRACTION_SEPARATION, outOfPlaneThickness=None)      
        

#assign section
p = mdb.models['bending-test-cohesive'].parts['PART-1']
region = p.sets['BEND-CLAMP']
p = mdb.models['bending-test-cohesive'].parts['PART-1']
p.SectionAssignment(region=region, sectionName='Q235', offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)

p = mdb.models['bending-test-cohesive'].parts['PART-1']
region = p.sets['REINFORCE-PIECE']
p = mdb.models['bending-test-cohesive'].parts['PART-1']
p.SectionAssignment(region=region, sectionName='reinforce-piece', offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)

p = mdb.models['bending-test-cohesive'].parts['PART-1']
region = p.sets['RESIN-POCKET']
p = mdb.models['bending-test-cohesive'].parts['PART-1']
p.SectionAssignment(region=region, sectionName='resin', offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
#assign laminate section
selection = ['lamina-N45D','lamina-0D','lamina-45D','lamina-90D']
p = mdb.models['bending-test-cohesive'].parts['PART-1']
region = p.sets['LAYER-1']
p.SectionAssignment(region=region, sectionName=selection[int(SQ[0])+1], offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
region = p.sets['LAYER-2']
p.SectionAssignment(region=region, sectionName=selection[int(SQ[1])+1], offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
region = p.sets['LAYER-3']
p.SectionAssignment(region=region, sectionName=selection[int(SQ[2])+1], offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
region = p.sets['LAYER-4']
p.SectionAssignment(region=region, sectionName=selection[int(SQ[3])+1], offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
region = p.sets['LAYER-5']
p.SectionAssignment(region=region, sectionName=selection[int(SQ[4])+1], offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
region = p.sets['LAYER-6']
p.SectionAssignment(region=region, sectionName=selection[int(SQ[5])+1], offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
region = p.sets['LAYER-7']
p.SectionAssignment(region=region, sectionName=selection[int(SQ[6])+1], offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
region = p.sets['LAYER-8']
p.SectionAssignment(region=region, sectionName=selection[int(SQ[7])+1], offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
region = p.sets['LAYER-9']
p.SectionAssignment(region=region, sectionName=selection[int(SQ[8])+1], offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
region = p.sets['LAYER-10']
p.SectionAssignment(region=region, sectionName=selection[int(SQ[9])+1], offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
region = p.sets['LAYER-11']
p.SectionAssignment(region=region, sectionName=selection[int(SQ[10])+1], offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
region = p.sets['LAYER-12']
p.SectionAssignment(region=region, sectionName=selection[int(SQ[11])+1], offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
region = p.sets['LAYER-13']
p.SectionAssignment(region=region, sectionName=selection[int(SQ[12])+1], offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
region = p.sets['LAYER-14']
p.SectionAssignment(region=region, sectionName=selection[int(SQ[13])+1], offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
region = p.sets['LAYER-15']
p.SectionAssignment(region=region, sectionName=selection[int(SQ[14])+1], offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
region = p.sets['LAYER-16']
p.SectionAssignment(region=region, sectionName=selection[int(SQ[15])+1], offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
region = p.sets['LAYER-17']
p.SectionAssignment(region=region, sectionName=selection[int(SQ[16])+1], offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
region = p.sets['LAYER-18']
p.SectionAssignment(region=region, sectionName=selection[int(SQ[17])+1], offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
region = p.sets['LAYER-19']
p.SectionAssignment(region=region, sectionName=selection[int(SQ[18])+1], offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
region = p.sets['LAYER-20']
p.SectionAssignment(region=region, sectionName=selection[int(SQ[19])+1], offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
region = p.sets['LAYER-21']
p.SectionAssignment(region=region, sectionName=selection[int(SQ[20])+1], offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
region = p.sets['LAYER-22']
p.SectionAssignment(region=region, sectionName=selection[int(SQ[21])+1], offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
region = p.sets['LAYER-23']
p.SectionAssignment(region=region, sectionName=selection[int(SQ[22])+1], offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
region = p.sets['LAYER-24']
p.SectionAssignment(region=region, sectionName=selection[int(SQ[23])+1], offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
region = p.sets['LAYER-25']
p.SectionAssignment(region=region, sectionName=selection[int(SQ[24])+1], offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
region = p.sets['LAYER-26']
p.SectionAssignment(region=region, sectionName=selection[int(SQ[25])+1], offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
region = p.sets['LAYER-27']
p.SectionAssignment(region=region, sectionName=selection[int(SQ[26])+1], offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
region = p.sets['LAYER-28']
p.SectionAssignment(region=region, sectionName=selection[int(SQ[27])+1], offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
#assign cohesive section
p = mdb.models['bending-test-cohesive'].parts['PART-1']
PDL_length = len(PDL)-2
PDL_index_list = range(PDL_length)
for name_index in PDL_index_list:
    section_name = "COHESIVESEAM-" + str(int(name_index)+1) + "-ELEMENTS"
    region = p.sets[section_name]
    p.SectionAssignment(region=region, sectionName='cohesive', offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)        

#edit step
mdb.models['bending-test-cohesive'].ExplicitDynamicsStep(name='Step-1', previous='Initial', timePeriod=0.1, improvedDtMethod=ON)
mdb.models['bending-test-cohesive'].fieldOutputRequests['F-Output-1'].setValues(variables=('S', 'E', 'U', 'RF', 'CSTRESS', 'DAMAGEFT', 'DAMAGEFC', 'DAMAGEMT', 'DAMAGEMC', 'SDEG', 'DMICRT', 'SDV', 'STATUS'), numIntervals=500)  

#interaction
a = mdb.models['bending-test-cohesive'].rootAssembly
n1 = a.instances['PART-1-1'].nodes
a.ReferencePoint(point=n1[65478])
a = mdb.models['bending-test-cohesive'].rootAssembly
n11 = a.instances['PART-1-1'].nodes
a.ReferencePoint(point=n11[66109])
a = mdb.models['bending-test-cohesive'].rootAssembly
n1 = a.instances['PART-1-1'].nodes
a.ReferencePoint(point=n1[64809])
a = mdb.models['bending-test-cohesive'].rootAssembly
r1 = a.referencePoints
refPoints1=(r1[4], )
a.Set(referencePoints=refPoints1, name='RF1')
#: The set 'RF1' has been created (1 reference point).
a = mdb.models['bending-test-cohesive'].rootAssembly
r1 = a.referencePoints
refPoints1=(r1[5], )
a.Set(referencePoints=refPoints1, name='RF2')
#: The set 'RF2' has been created (1 reference point).
a = mdb.models['bending-test-cohesive'].rootAssembly
r1 = a.referencePoints
refPoints1=(r1[6], )
a.Set(referencePoints=refPoints1, name='RF3')
#: The set 'RF3' has been created (1 reference point).
a = mdb.models['bending-test-cohesive'].rootAssembly
e1 = a.instances['PART-1-1'].elements
elements1 = e1[95510:95990]+e1[97430:97910]
region2=regionToolset.Region(elements=elements1)
a = mdb.models['bending-test-cohesive'].rootAssembly
region1=a.sets['RF1']
mdb.models['bending-test-cohesive'].RigidBody(name='Constraint-1', refPointRegion=region1, bodyRegion=region2, refPointAtCOM=ON)
a = mdb.models['bending-test-cohesive'].rootAssembly
e1 = a.instances['PART-1-1'].elements
elements1 = e1[95990:96950]
region2=regionToolset.Region(elements=elements1)
a = mdb.models['bending-test-cohesive'].rootAssembly
region1=a.sets['RF2']
mdb.models['bending-test-cohesive'].RigidBody(name='Constraint-2', refPointRegion=region1, bodyRegion=region2, refPointAtCOM=ON)
a = mdb.models['bending-test-cohesive'].rootAssembly
e1 = a.instances['PART-1-1'].elements
elements1 = e1[95030:95510]+e1[96950:97430]
region2=regionToolset.Region(elements=elements1)
a = mdb.models['bending-test-cohesive'].rootAssembly
region1=a.sets['RF3']
mdb.models['bending-test-cohesive'].RigidBody(name='Constraint-3', refPointRegion=region1, bodyRegion=region2, refPointAtCOM=ON)
a = mdb.models['bending-test-cohesive'].rootAssembly
f1 = a.instances['PART-1-1'].elements
face4Elements1 = f1[95530:95550]+f1[95610:95630]+f1[95730:95750]+f1[95850:95870]+f1[97490:97510]+f1[97730:97750]+f1[97790:97810]+f1[97830:97850]
face5Elements1 = f1[95570:95590]+f1[95810:95830]+f1[95870:95890]+f1[95910:95930]+f1[97450:97470]+f1[97530:97550]+f1[97650:97670]+f1[97770:97790]
a.Surface(face4Elements=face4Elements1, face5Elements=face5Elements1, name='clamp1')
#: The surface 'clamp1' has been created (320 mesh faces).
a = mdb.models['bending-test-cohesive'].rootAssembly
f1 = a.instances['PART-1-1'].elements
face4Elements1 = f1[96070:96090]+f1[96210:96270]+f1[96650:96670]+f1[96790:96830]+f1[96910:96930]
face5Elements1 = f1[96170:96190]+f1[96310:96350]+f1[96430:96450]+f1[96550:96570]+f1[96690:96750]
a.Surface(face4Elements=face4Elements1, face5Elements=face5Elements1, name='clamp2')
#: The surface 'clamp2' has been created (320 mesh faces).
a = mdb.models['bending-test-cohesive'].rootAssembly
f1 = a.instances['PART-1-1'].elements
face4Elements1 = f1[95150:95170]+f1[95210:95250]+f1[95330:95350]+f1[96950:96970]+f1[97110:97130]+f1[97190:97210]+f1[97330:97350]
face5Elements1 = f1[95030:95050]+f1[95190:95210]+f1[95270:95290]+f1[95410:95430]+f1[97070:97090]+f1[97130:97170]+f1[97250:97270]
a.Surface(face4Elements=face4Elements1, face5Elements=face5Elements1, name='clamp3')
#: The surface 'clamp3' has been created (320 mesh faces).
a = mdb.models['bending-test-cohesive'].rootAssembly
f1 = a.instances['PART-1-1'].elements
face1Elements1 = f1[156:312]+f1[3510:4537]+f1[32266:33293]
a.Surface(face1Elements=face1Elements1, name='laminate-up')
#: The surface 'laminate-up' has been created (2210 mesh faces).
a = mdb.models['bending-test-cohesive'].rootAssembly
f1 = a.instances['PART-1-1'].elements
face2Elements1 = f1[31239:32266]
a.Surface(face2Elements=face2Elements1, name='laminate-low2')
#: The surface 'laminate-low2' has been created (1027 mesh faces).
a = mdb.models['bending-test-cohesive'].rootAssembly
f1 = a.instances['PART-1-1'].elements
face2Elements1 = f1[105060:105710]
a.Surface(face2Elements=face2Elements1, name='laminate-low3')
#: The surface 'laminate-low3' has been created (650 mesh faces).
mdb.models['bending-test-cohesive'].ContactProperty('IntProp-1')
mdb.models['bending-test-cohesive'].interactionProperties['IntProp-1'].TangentialBehavior(formulation=PENALTY, directionality=ISOTROPIC, slipRateDependency=OFF, 
    pressureDependency=OFF, temperatureDependency=OFF, dependencies=0, table=((0.1, ), ), shearStressLimit=None, maximumElasticSlip=FRACTION, fraction=0.005, elasticSlipStiffness=None)
mdb.models['bending-test-cohesive'].interactionProperties['IntProp-1'].NormalBehavior(pressureOverclosure=HARD, allowSeparation=ON, constraintEnforcementMethod=DEFAULT)
#: The interaction property "IntProp-1" has been created.
a = mdb.models['bending-test-cohesive'].rootAssembly
region1=a.surfaces['laminate-up']
a = mdb.models['bending-test-cohesive'].rootAssembly
region2=a.surfaces['clamp1']
mdb.models['bending-test-cohesive'].SurfaceToSurfaceContactExp(name ='Int-1', createStepName='Initial', master = region1, slave = region2, mechanicalConstraint=KINEMATIC, sliding=FINITE, 
    interactionProperty='IntProp-1', initialClearance=OMIT, datumAxis=None, clearanceRegion=None)
#: The interaction "Int-1" has been created.
a = mdb.models['bending-test-cohesive'].rootAssembly
region1=a.surfaces['laminate-low2']
a = mdb.models['bending-test-cohesive'].rootAssembly
region2=a.surfaces['clamp2']
mdb.models['bending-test-cohesive'].SurfaceToSurfaceContactExp(name ='Int-2', createStepName='Initial', master = region1, slave = region2, mechanicalConstraint=KINEMATIC, sliding=FINITE, 
    interactionProperty='IntProp-1', initialClearance=OMIT, datumAxis=None, clearanceRegion=None)
#: The interaction "Int-2" has been created.
a = mdb.models['bending-test-cohesive'].rootAssembly
region1=a.surfaces['laminate-low3']
a = mdb.models['bending-test-cohesive'].rootAssembly
region2=a.surfaces['clamp3']
mdb.models['bending-test-cohesive'].SurfaceToSurfaceContactExp(name ='Int-3', createStepName='Initial', master = region1, slave = region2, mechanicalConstraint=KINEMATIC, sliding=FINITE, 
    interactionProperty='IntProp-1', initialClearance=OMIT, datumAxis=None, clearanceRegion=None)
#: The interaction "Int-3" has been created.


#loads
a = mdb.models['bending-test-cohesive'].rootAssembly
region = a.sets['RF2']
mdb.models['bending-test-cohesive'].EncastreBC(name='constraint2', createStepName='Initial', region=region, localCsys=None)   
a = mdb.models['bending-test-cohesive'].rootAssembly
region = a.sets['RF3']
mdb.models['bending-test-cohesive'].EncastreBC(name='constraint3', createStepName='Initial', region=region, localCsys=None)
a = mdb.models['bending-test-cohesive'].rootAssembly
region = a.sets['RF1']
mdb.models['bending-test-cohesive'].DisplacementBC(name='load', createStepName='Initial', region=region, u1=SET, u2=SET, u3=SET, ur1=SET, ur2=SET, ur3=SET, amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)

mdb.models['bending-test-cohesive'].SmoothStepAmplitude(name='Amp-1', timeSpan=STEP, data=((0.0, 0.0), (0.01, 1.0)))
mdb.models['bending-test-cohesive'].boundaryConditions['load'].setValuesInStep(stepName='Step-1', u3=15.0, amplitude='Amp-1')


#assign elements type
elemType1 = mesh.ElemType(elemCode=C3D8, elemLibrary=EXPLICIT, secondOrderAccuracy=OFF, distortionControl=DEFAULT)
p = mdb.models['bending-test-cohesive'].parts['PART-1']
z1 = p.elements
elems1 = z1[95030:97910]
pickedRegions =(elems1, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, ))

elemType1 = mesh.ElemType(elemCode=COH3D8, elemLibrary=EXPLICIT, elemDeletion=ON)
p = mdb.models['bending-test-cohesive'].parts['PART-1']
z1 = p.elements
elems1 = z1[48698:95030]
pickedRegions =(elems1, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, ))

elemType1 = mesh.ElemType(elemCode=SC8R, elemLibrary=EXPLICIT, secondOrderAccuracy=OFF, hourglassControl=DEFAULT, elemDeletion=ON)
p = mdb.models['bending-test-cohesive'].parts['PART-1']
z1 = p.elements
elems1 = z1[156:48698]
pickedRegions =(elems1, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, ))

elemType1 = mesh.ElemType(elemCode=C3D6, elemLibrary=EXPLICIT, secondOrderAccuracy=OFF, distortionControl=DEFAULT, elemDeletion=ON)
p = mdb.models['bending-test-cohesive'].parts['PART-1']
z1 = p.elements
elems1 = z1[0:156]
pickedRegions =(elems1, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, ))

elemType1 = mesh.ElemType(elemCode=C3D8I, elemLibrary=EXPLICIT, secondOrderAccuracy=OFF, distortionControl=DEFAULT)
p = mdb.models['bending-test-cohesive'].parts['PART-1']
z1 = p.elements
elems1 = z1[97910:105710]
pickedRegions =(elems1, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, ))


#field and history outputs
mdb.models['bending-test-cohesive'].historyOutputRequests['H-Output-1'].setValues(numIntervals=500)
regionDef=mdb.models['bending-test-cohesive'].rootAssembly.sets['RF1']
mdb.models['bending-test-cohesive'].HistoryOutputRequest(name='H-Output-2', createStepName='Step-1', variables=('U3', ), numIntervals=500, region=regionDef, sectionPoints=DEFAULT, rebar=EXCLUDE)
mdb.models['bending-test-cohesive'].HistoryOutputRequest(name='H-Output-3', createStepName='Step-1', variables=('CFN3', ), numIntervals=500, interactions=('Int-1', ), sectionPoints=DEFAULT, rebar=EXCLUDE)

a = mdb.models['bending-test-cohesive'].rootAssembly
mdb.Job(name='bending-test-cohesive', model='bending-test-cohesive', description='', type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, 
    queue=None, memory=90, memoryUnits=PERCENTAGE, explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, modelPrint=OFF, 
    contactPrint=OFF, historyPrint=OFF, userSubroutine='', scratch='', resultsFormat=ODB, parallelizationMethodExplicit=DOMAIN, numDomains=48, 
    activateLoadBalancing=False, multiprocessingMode=DEFAULT, numCpus=48)
    
mdb.save()
mdb.jobs['bending-test-cohesive'].submit(consistencyChecking=OFF)
