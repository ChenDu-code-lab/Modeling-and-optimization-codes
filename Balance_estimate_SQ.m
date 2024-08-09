function Decision_factor = Balance_estimate_SQ(random_SQ)
num45 = sum(random_SQ(:) == 1);num_45 = sum(random_SQ(:) == -1);
if num45 ~= num_45
    Decision_factor = 0;
else
    Decision_factor = 1;
end