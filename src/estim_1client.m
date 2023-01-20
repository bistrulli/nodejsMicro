clear

load('../data/acmeAir.py_full_10b.mat');
load('../data/acmeAir.py_full_data_out');
load('/Users/emilio-imt/git/nodejsMicro/data/ICDCS/validation/m1/validation_2.mat');


msname=strtrim(string(ms));
%msname(1)=[];
st_est=zeros(1,length(msname));


msdata=readData("../data/ICDCS/validation/10_client/*.csv");

%mi mappa gli indici della matrice di routing in quella delle misure che st
% sto prendendo adesso
mappingMat=zeros(length(msname),1);
% mappingMat2=zeros(length(msname),1);

for m=2:length(msname)
    for i=1:size(msdata,2)
        if(msdata(i).name==sprintf("%s.csv",msname(m)))
            mappingMat(m)=i;
        end
    end
end

RTm=zeros(1,size(mappingMat,1))-1;
Tm=zeros(1,size(mappingMat,1))-1;
for i=2:size(mappingMat,1)
    %disp([msname(i),msdata(mappingMat(i)).name])
    RTm(1,i)=mean(msdata(mappingMat(i)).rt);
    Tm(1,i)=mean(msdata(mappingMat(i)).tr);
end



P2=round(P2); 
for i=2:size(P2,1)
    for j=2:size(P2,2)
        %st_est(i)=st_est(i)+mean(msdata(mappingMat(j)).rt())*P2(i,j);
        st_est(i)=st_est(i)+RTm(1,j)*P2(i,j);
    end
    st_est(i)=RTm(1,i)-st_est(i);
    disp([msname(i),st_est(i)]);
end

rates=1./(st_est');

MU=zeros(1,30);
MU([5,6,9,12,15,20,23,24,29,30])=rates([3,2,4,5,9,6,10,7,8,1]);
MU(end)=5;
save("params.mat","MU");