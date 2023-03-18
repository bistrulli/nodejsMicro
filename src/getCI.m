function [CI] = getCI(X)
SEM = std(X)/sqrt(length(X));
ts = tinv([0.025  0.975],length(X)-1);
CI = mean(X) + ts*SEM;
end