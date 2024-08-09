function [output_args] = runabaqus(Path,InputFile)
inputFile = ['Abaqus cae nogui=',InputFile]; 
t0 = tic;
MatlabPath = pwd();     
cd(Path);     
[output_args] = system(inputFile); 
pause(5)
cd(MatlabPath);
if (exist([Path,'\',InputFile,'.lck'],'file') == 2)
    while exist ([Path,'\',InputFile,'.lck'],'file') == 2
        t = toc(t0);
        h = fix(t/3600);
        m = fix(mod(t,3600)/60);
        sec = fix(mod(mod(t,3600),60));
        pause(1)
        fprintf('-----------ABAQUS calculating-----------\n    time costed %d:%d:%d\n',h,m,sec);
    end
    fprintf('-----------ABAQUS complete-----------\n    time costed %d:%d:%d\n',h,m,sec);
else
    fprintf('\n runabaqus error:InputFile submmit failed\n')
end
end