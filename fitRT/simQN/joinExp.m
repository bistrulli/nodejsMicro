clear

dataFiles=["../../data/acmeAir/acme_full/acmeAir.py_full_6b.mat",...
       "../../data/acmeAir/acme_full/acmeAir.py_full_7b.mat",...
       "../../data/acmeAir/acme_full/acmeAir.py_full_8b.mat",...
       "../../data/acmeAir/acme_full/acmeAir.py_full_9b.mat"];

Cli=[];
RTm=[];
Tm=[];
rtCI=[];
trCI=[];
NC=[];
for i=1:length(dataFiles)
    data=load(dataFiles(i));
    CIdx=sum(sum(data.RTm,2)~=0);
    
    Cli=cat(2,Cli,data.Cli(1:CIdx));
    RTm=cat(1,RTm,data.RTm(1:CIdx,:));
    Tm=cat(1,Tm,data.Tm(1:CIdx,:));
    rtCI=cat(1,rtCI,data.rtCI(1:CIdx,:));
    trCI=cat(1,trCI,data.trCI(1:CIdx,:));
    NC=cat(1,NC,data.NC([1:CIdx],:));
end

ms=data.ms;
clear data i dataFiles CIdx;

save("../../data/acmeAir.py_full_data.mat");

% 
% e1=load("../../data/acmeAir/acme_full/acmeAir.py_full_6b.mat");
% e2=load("../../data/acmeAir/acme_full/acmeAir.py_full_7b.mat");
% e3=load("../../data/acmeAir/acme_full/acmeAir.py_full_8b.mat");
% 
% e1CIdx=sum(sum(e1.RTm,2)~=0);
% e2CIdx=sum(sum(e2.RTm,2)~=0);
% e3CIdx=sum(sum(e3.RTm,2)~=0);
% 
% 
% Cli=cat(2,e1.Cli([1:e1CIdx]),e2.Cli(1:e2CIdx),e3.Cli(1:e3CIdx));
% RTm=cat(1,e1.RTm([1:e1CIdx],:),e2.RTm(1:e2CIdx,:),e3.RTm(1:e3CIdx,:));
% Tm=cat(1,e1.Tm([1:e1CIdx],:),e2.Tm(1:e2CIdx,:),e3.Tm(1:e3CIdx,:));
% rtCI=cat(1,e1.rtCI([1:e1CIdx],:),e2.rtCI(1:e2CIdx,:),e3.rtCI(1:e3CIdx,:));
% trCI=cat(1,e1.trCI([1:e1CIdx],:),e2.trCI(1:e2CIdx,:),e3.trCI(1:e3CIdx,:));
% NC=cat(1,e1.NC([1:e1CIdx],:),e2.NC([1:e2CIdx],:),e3.NC(1:e3CIdx,:));
% ms=e1.ms;
% 
% 
% clear e1 e2 e3
% 
% save("../../data/acmeAir.py_full_data.mat");