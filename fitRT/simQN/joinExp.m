clear

e1=load("../../data/acmeAir/acmeAir.py_full_7b.mat");
e2=load("../../data/acmeAir/acmeAir.py_full_6b.mat");

e1CIdx=sum(sum(e1.RTm,2)~=0);
e2CIdx=sum(sum(e2.RTm,2)~=0);


Cli=cat(2,e1.Cli([1:e1CIdx]),e2.Cli(1:e2CIdx));
RTm=cat(1,e1.RTm([1:e1CIdx],:),e2.RTm(1:e2CIdx,:));
Tm=cat(1,e1.Tm([1:e1CIdx],:),e2.Tm(1:e2CIdx,:));
rtCI=cat(1,e1.rtCI([1:e1CIdx],:),e2.rtCI(1:e2CIdx,:));
trCI=cat(1,e1.trCI([1:e1CIdx],:),e2.trCI(1:e2CIdx,:));
NC=cat(1,e1.NC([1:e1CIdx],:),e2.NC([1:e2CIdx],:));
ms=e1.ms;


clear e1 e2

save("../../data/acmeAir.py_full_data.mat");