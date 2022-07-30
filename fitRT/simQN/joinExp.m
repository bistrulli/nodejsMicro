clear

e1=load("/Users/emilio/git/nodejsMicro/data/3tier.mat");
e2=load("/Users/emilio/git/nodejsMicro/data/3tier2.mat");

e1CIdx=sum(sum(e1.RTm,2)~=0);
e2CIdx=sum(sum(e2.RTm,2)~=0);


Cli=cat(2,e1.Cli([1:e1CIdx]),e2.Cli(e1CIdx+1:end));
RTm=cat(1,e1.RTm([1:e1CIdx],:),e2.RTm(:,:));
Tm=cat(1,e1.Tm([1:e1CIdx],:),e2.Tm(:,:));
rtCI=cat(1,e1.rtCI([1:e1CIdx],:),e2.rtCI(:,:));
trCI=cat(1,e1.trCI([1:e1CIdx],:),e2.trCI(:,:));
%NC=cat(1,e1.NC([1:e1CIdx],:),e2.NC([1:e2CIdx],:));
ms=e1.ms;


clear e1 e2

save("/Users/emilio/git/nodejsMicro/data/3tier_all.mat");