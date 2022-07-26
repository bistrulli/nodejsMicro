clear

k=100;

X0=[10,0]*k;
MU=[1,1];
S=[1,1]*k;
P=[0 1.;
   1 0];
TF=2000;
dt=0.1;
rep=100;

X=QN(X0,S,P,MU,TF,rep,dt);
Xm=mean(X,3);
[t,y,T,RT]=QN_ODE(X0,S,P,MU,inf);

