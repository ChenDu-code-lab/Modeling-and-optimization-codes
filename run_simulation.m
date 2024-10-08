function [MaxU,MaxCFN,U,CFN] = run_simulation(Path)
HMPath = Path;
HMInputFile = '\bending-PD-section.tcl';
[HMoutput_args] = runhypermesh(HMPath,HMInputFile);
HMInputFile = '\bending-CT-layer-section.tcl';
[HMoutput_args] = runhypermesh(HMPath,HMInputFile);
HMInputFile = '\bending-pretreatment-model.tcl';
[HMoutput_args] = runhypermesh(HMPath,HMInputFile);
InputFile = 'E:\User\DC\bending-optimization\abaqus-analysis\bending-abaqus-analysis-cohesive.py';
inputFile = ['Abaqus cae nogui=',InputFile];
[output_args] = system(inputFile);
step = 'Step-1';
Path = 'E:\User\DC\bending-optimization\abaqus-analysis';
OdbFile = 'bending-test-cohesive.odb';
get_history_output(Path,OdbFile,step);
result = textread('E:\User\DC\bending-optimization\optimization algorithm\result-U.txt','%f');
U = result(:,1);
result = textread('E:\User\DC\bending-optimization\optimization algorithm\result-CFN.txt','%f');
CFN = result(:,1);
[MaxU,MaxCFN] = Ultimate_resistance(U,CFN);
