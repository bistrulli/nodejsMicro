clear
load('/Users/emilio/git/nodejsMicro/data/3tier_test_java_jitless_worker.mat')

RT=zeros(size(Cli,2),3);

NT=[inf,inf,inf];
% NC=[inf,1,1];
X0=zeros(1,9);

MU=1000./[flip(diff(flip(RTm(1,:)))),RTm(1,3)];
%MU=[9.7355 7.513859495775013 9.725773227044295];
%sMU=[22.60809449606986 4.910126034003662 38.93750429888124];

for i=size(Cli,2):size(Cli,2)
    
    X0(1)=Cli(i);
    disp(X0(1))
 
    TF=10000;
    rep=1;
    dt=10^-1;
    
    
    X=lqn(X0,MU,NT,NC(i,:),TF,rep,dt);
    T=linspace(1,size(X,2),size(X,2));
    
    Xm=cumsum(X,2)./T;
    
    RT3=sum(Xm([6],end))/(X(9,end)/TF);
    RT2=sum(Xm([4],end))/(X(8,end)/TF);
    RT1=Xm(1,end)/(X(7,end)/TF);
    
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
