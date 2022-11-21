X0=zeros(1,8);
X0(1)=10;
MU=zeros(1,8);
MU(1,[1,4,6])=[1,1,1];
NC=[1,inf];

rep=1;
dt=0.1;
TF=1000;

X=msMPP(X0,MU,NC,TF,rep,dt);
Xm=mean(X,3)';


plot(cumsum(Xm(:,1))'./linspace(1,size(Xm(:,1),1),size(Xm(:,1),1)));