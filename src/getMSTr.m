function tr=getMSTr(dataPath)
cmp_evt = sortrows(readmatrix(dataPath),2);
kidx=1;
tcmp=0;
tr=[];
i=1;
initTime=min(cmp_evt(:,1));
endTime=max(cmp_evt(:,2));
while(i<=size(cmp_evt,1))
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