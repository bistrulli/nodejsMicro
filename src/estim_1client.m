clear

load('../data/acmeAir.py_full_10b.mat');
load('../data/acmeAir.py_full_data_out');
load('../data/acmeAir.py_full_1_icdcs_val_server.mat');

msname=strtrim(string(ms)); 
st_est=zeros(1,length(msname));

% msdata=readData("../data/ICDCS/*.csv");
% 
% 
% 
% 
% %mi mappa gli indici della matrice di routing in quella delle misure che st
% % sto prendendo adesso
% mappingMat=zeros(length(msname),1);
% mappingMat2=zeros(length(msname),1);
% 
% for m=1:length(msname)
%     for i=1:length(msname)
%         if(msdata(i).name==sprintf("%s.csv",msname(m)))
%             mappingMat(m)=i;
%         end
%     end
% end
% 

P2=round(P2); 
for i=1:size(P2,1)
    disp(msname(i))
    for j=1:size(P2,2)
        %st_est(i)=st_est(i)+mean(msdata(mappingMat(j)).rt())*P2(i,j);
        st_est(i)=st_est(i)+RTm(1,j)*P2(i,j);
    end
    st_est(i)=RTm(1,i)-st_est(i);
end

rates=1./(st_est'/1000);

MU=zeros(1,30);
MU([5,6,9,12,15,20,23,24,29,30])=rates([3,2,4,5,9,6,10,7,8,1]);

save("params.mat","MU");