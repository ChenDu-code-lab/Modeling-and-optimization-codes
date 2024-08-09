function Decision_factor = Internal_continuity_PD(random_SSTins)
SSTins_length = size(random_SSTins,2);
for n = 4:SSTins_length
    if random_SSTins(n) ~= 0 && random_SSTins(n-1) ~= 0 && random_SSTins(n-2) ~= 0 && random_SSTins(n-3) ~= 0
        Decision_factor = 0;
        break
    else
        Decision_factor = 1;
    end
end