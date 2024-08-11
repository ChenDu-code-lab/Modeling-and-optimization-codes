function random_initialSQ = generate_initialSQ(Optional_degree,random_PDL)
Decision_factor = 0;Decision_factor1 = 0;size_random_PDL = size(random_PDL,2);
while Decision_factor1 ~= 1
    Nply_45 = randperm(size_random_PDL/4,1);ply_45 = ones(1,Nply_45);ply_N45 = ones(1,Nply_45)*(-1);
    degree = [0,2];ply_residue = degree(randi(numel(degree),1,size_random_PDL/2-Nply_45*2));
    random_initialSQ = [ply_residue,ply_45,ply_N45];randIndex = randperm(size(random_initialSQ,2));
    random_initialSQ = random_initialSQ(randIndex);random_SQ = [random_initialSQ,flip(random_initialSQ)];
    while Decision_factor ~= 1
        Decision_factor = Tenrule_estimate_SQ(random_SQ);
        if Decision_factor ~= 1
            break
        end
%        Decision_factor = Disorientation_estimate_SQ(random_SQ);
%        if Decision_factor ~= 1
%            break
%        end
        Decision_factor = Contiguity_estimate_SQ(random_SQ);
        if Decision_factor ~= 1
            break
        end
        Decision_factor = Damtol_estimate_SQ(random_SQ);
        if Decision_factor ~= 1
            break
        end
        Decision_factor1 = 1;
    end
end
random_initialSQ = random_SQ;
Path = 'E:\User\DC\bending-optimization\abaqus-analysis';ReqFile = [Path,'\stacking-sequence.txt'];
fid = fopen(ReqFile,'w');
SQsize = size(random_initialSQ,2);
for i = 1:SQsize
    fprintf(fid,'%3d,',random_initialSQ(i));
end
fclose(fid);