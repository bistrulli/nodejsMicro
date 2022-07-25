clear

X0=[10,0,0];
MU=[80,5,30];
S=[inf,4,4];
P=[0 1. 0 ;
   0 0  1.;
   1. 0 0];
TF=2000;
dt=0.1;
rep=100;

X=QN(X0,S,P,MU,TF,rep,dt);
Xm=mean(X,3);
[t,y,T,RT]=QN_ODE(X0,S,P,MU,inf);
