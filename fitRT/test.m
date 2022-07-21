clear
load('/Users/emilio/git/nodejsMicro/data/3tier_test_java.mat')

RT=zeros(size(Cli,2),3);

NT=[inf,1,1];
NC=[inf,1,1];
X0=zeros(1,6);

MU=1000./[flip(diff(flip(RTm(1,:)))),RTm(1,3)];
MU=[1/0.1,1/0.128,1/0.118];

for i=1:size(Cli,2)
    
    X0(1)=Cli(i);
 
    TF=10000;
    rep=1;
    dt=10^-1;
    
    
    X=lqn(X0,MU,NT,NC,TF,rep,dt);
    T=linspace(1,size(X,2),size(X,2));
    
    Xm=cumsum(X,2)./T;
    
    RT3=sum(Xm([5,6],end))/(MU(3)*min(Xm(6,end),NC(3)));
    RT2=sum(Xm([2,3,4],end))/(MU(2)*min(Xm(4,end),NC(2)));
    RT1=Xm(1,end)/(MU(1)*min(Xm(1,end),NC(1)));
    
    RT(i,:)=[RT1+RT2+RT3,RT2+RT3,RT3];
    
end

figure
hold on
plot(RTm(:,1)/1000,"-.")
plot(RT(:,1))

figure
hold on
plot(RTm(:,2)/1000,"-.")
plot(RT(:,2))

figure
hold on
plot(RTm(:,3)/1000,"-.")
plot(RT(:,3))
