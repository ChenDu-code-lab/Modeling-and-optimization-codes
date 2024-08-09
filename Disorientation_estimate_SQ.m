function Decision_factor = Disorientation_estimate_SQ(random_SQ)
total_ply = size(random_SQ,2);
for n = 2:total_ply-1
    deta_orientation1 = abs(random_SQ(n) - random_SQ(n-1));
    deta_orientation2 = abs(random_SQ(n+1) - random_SQ(n));
    if deta_orientation1 > 1 || deta_orientation2 > 1
        Decision_factor = 0;
        break
    else
        Decision_factor = 1;
    end
end