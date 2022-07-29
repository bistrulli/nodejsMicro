clear

X0=[1,0,0];
MU=[1/0.2,1/0.2,1/0.033];
S=[inf,20,2];
P=[0,1.,0;
    0,0,1;
    1,0,0;];
TF=20000;
dt=0.1;
rep=1;

pop=round(linspace(1,100,30));

Xsim=zeros(size(pop,2),3);
Xode=zeros(size(pop,2),3);

for i=1:size(pop,2)
    X0(1)=pop(1,i);
    X=QN(X0,S,P,MU,TF,rep,dt);
    Xm=(cumsum(X,2)./linspace(1,size(X,2),size(X,2)))';
    [t,y,T,RT]=QN_ODE(X0,S,P,MU,inf);
    Xsim(i,:)=Xm(end,:);
    Xode(i,:)=y(end,:);
end

ax = axes;
ax.ColorOrder = [1 0 0; 1 0 0; 0,0,1;0,0,1;0 1 0;0 1 0;];
%ax.LineStyleOrder = {'-','-.','-','-.','-','-.'};
hold on

for i=1:size(Xsim,2) 
    plot(Xsim(:,i),"--","linewidth",1.2);
    plot(Xode(:,i),"linewidth",1.2);
end

