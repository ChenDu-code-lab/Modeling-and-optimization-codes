function [HMoutput_args] = runhypermesh(HMPath,HMInputFile)
path = [HMPath,HMInputFile];
HMinputfile = ['D:\Program_Files\Altair\2019\hm\bin\win64\hmbatch.exe  -tcl ',path];   %hmopengl.exe;hmbatch.exe
MatlabPath = pwd();  
cd(HMPath);      
[HMoutput_args] = system(HMinputfile);     
cd(MatlabPath);   