function tr=getMSTr(dataPath)
cmp_evt = readmatrix(dataPath);
kidx=1;
tcmp=0;
tr=[];
i=1;
initTime=min(cmp_evt(:,1));
while(i<=size(cmp_evt,1))
    disp((cmp_evt(i,2)-initTime)/10^3)
    if((kidx-1)<=(cmp_evt(i,2)-initTime)/10^3 && (cmp_evt(i,2)-initTime)/10^3<=(kidx))
        tcmp=tcmp+1;
        i=i+1;
    else
        tr=[tr,tcmp];
        tcmp=0;
        kidx=kidx+1;
    end
end
end