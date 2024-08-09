#-*-coding: UTF-8 -*-
from abaqus import *
from abaqusConstants import *
from odbAccess import *
from caeModules import *
from driverUtils import executeOnCaeStartup
from numpy import random
import os
import sys
executeOnCaeStartup()
#sys.path.append(r'E:/python-3.7.0/Lib/site-packages')
#import xlsxwriter

f = open('E:/User/DC/bending-optimization/optimization algorithm/req.txt','r')
req = f.readline()
f.close()
req = req.split(',')
path = req[0]+'/'+req[1]    
step = req[2]

odb = openOdb(path = path)

step_n = odb.steps[step]
region=step_n.historyRegions['Node ASSEMBLY.1']
U_data=region.historyOutputs['U3'].data

odb = session.odbs['E:/User/DC/bending-optimization/abaqus-analysis/bending-test-cohesive.odb']
xy_result = session.XYDataFromHistory(name='F', odb=odb, outputVariableName='Total force due to contact pressure: CFN3     ASSEMBLY_LAMINATE-UP/ASSEMBLY_CLAMP1', steps=('Step-1', ), )
c1 = session.Curve(xyData=xy_result)
CFN_data=c1.data

with open('E:/User/DC/bending-optimization/optimization algorithm/result-U.txt','w') as f:
    for time1,U in U_data:
        f.write('%10.4E \n'%(U))

with open('E:/User/DC/bending-optimization/optimization algorithm/result-CFN.txt','w') as f:
    for time2,CFN in CFN_data:
        f.write('%10.4E \n'%(CFN))
        
        