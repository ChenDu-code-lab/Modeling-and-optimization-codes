function Decision_factor = Damtol_estimate_SQ(random_SQ)
if random_SQ(end) == 0 || random_SQ(end) == 2 || random_SQ(1) == 0 || random_SQ(1) == 2
    Decision_factor = 0;
else
    Decision_factor = 1;
end