clear

X0=zeros(1,9);
X0(1)=4;
MU=[1,1];
S=[inf,1];

rep=100;
TF=50;
dt=1;

P01=0.2;
P01A=0.0001;
P0E=1;
P=[P01,P01A,P0E];

X=QN(X0,S,P,MU,TF,rep,dt);
Xm=mean(X,3);
%Xss=(cumsum(X,2)./linspace(1,size(X,2),size(X,2)))';

T=Xm(end,end)/TF;
RT=(X(1,end)+X(3,end)+X(6,end))/T;