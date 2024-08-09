function Decision_factor = Tenrule_estimate_SQ(random_SQ)
Optional_degree = [0 1 -1 2];total_ply = size(random_SQ,2);
for i = 1: size(Optional_degree,2)
    degree_num = sum(random_SQ(:) == Optional_degree(i));
    percentage = degree_num/total_ply;
    if percentage >= 0.1
        Decision_factor = 1;
    else
        Decision_factor = 0;
        break
    end
end
