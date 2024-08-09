function Decision_factor = Contiguity_estimate_SQ(random_SQ)
total_ply = size(random_SQ,2);
for n = 5:total_ply
    if random_SQ(n-4) == random_SQ(n-3) && random_SQ(n-3) == random_SQ(n-2) && random_SQ(n-2) == random_SQ(n-1) && random_SQ(n-1) == random_SQ(n)
        Decision_factor = 0;
        break
    else
        Decision_factor = 1;
    end
end
