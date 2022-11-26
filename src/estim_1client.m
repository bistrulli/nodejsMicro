clear

load('../data/acmeAir.py_full_10b.mat');
load('../data/acmeAir.py_full_data_out');

msdata=readData("../data/ICDCS/*.csv");
msname=strtrim(string(ms));

st_est=zeros(1,length(msname));




%mi mappa gli indici della matrice di routing in quella delle misure che st
% sto prendendo adesso
mappingMat=zeros(length(msname),1);
mappingMat2=zeros(length(msname),1);

for m=1:length(msname)
    for i=1:length(msname)
        if(msdata(i).name==sprintf("%s.csv",msname(m)))
            mappingMat(m)=i;
        end
    end
end

P2t=round(P2);

for i=1:size(P2,1)
    disp(msname(i))
    for j=1:size(P2,2)
        st_est(i)=st_est(i)+mean(msdata(mappingMat(j)).rt())*P2t(i,j);
    end
    st_est(i)=mean(msdata(mappingMat(i)).rt())-st_est(i);
end