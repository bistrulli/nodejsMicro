clear

e1=load("acmeAir.py_4b.mat");
e2=load("acmeAir.py_3b.mat");
e3=load("acmeAir.py_2b.mat");

e1CIdx=sum(sum(e1.RTm,2)~=0);
e2CIdx=sum(sum(e2.RTm,2)~=0);
e3CIdx=sum(sum(e3.RTm,2)~=0);

Cli=cat(2,e1.Cli([1:e1CIdx]),e2.Cli(1:e2CIdx),e3.Cli(1:e3CIdx));
RTm=cat(1,e1.RTm([1:e1CIdx],:),e2.RTm([1:e2CIdx],:),e3.RTm([1:e3CIdx],:));
Tm=cat(1,e1.Tm([1:e1CIdx],:),e2.Tm([1:e2CIdx],:),e3.Tm([1:e3CIdx],:));
NC=cat(1,e1.NC([1:e1CIdx],:),e2.NC([1:e2CIdx],:),e3.NC([1:e3CIdx],:));
ms=e1.ms;


clear e1 e2 e3

save("acmeair_data.mat")