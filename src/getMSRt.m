function rt=getMSRt(dataPath)
cmp_evt = readmatrix(dataPath);
rt=(cmp_evt(:,2)-cmp_evt(:,1))/10^3;
end