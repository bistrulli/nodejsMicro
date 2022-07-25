clear

X0=[0,300,0];
MU=[1,1,1];
S=[inf,1,2];
P=[0 1. 0 ;
   0 0  1.;
   1. 0 0];
TF=2000;
dt=0.1;
rep=100;

% X=QN(X0,S,P,MU,TF,rep,dt);
% Xm=mean(X,3);
[t,y,T,RT]=QN_ODE(X0,S,P,MU);
