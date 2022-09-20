clear
load("../../data/acmeAir.py_full_data_out.mat")
load("/Users/emilio/git/nodejsMicro/data/acmeAir.py_full_4wi.mat");

% P=[0,1,0,1,1;
%    0,0,1,0,0;
%    0,0,0,0,0;
%    0,0,0,0,0;
%    0,0,0,0,0;];

% P2=[0,1,0,1,1,0,1,1,1,0;
%     0,0,1,0,0,0,0,0,0,0;
%     0,0,0,0,0,0,0,0,0,0;
%     0,0,0,0,0,0,0,0,0,0;
%     0,0,0,0,0,0,0,0,0,0;
%     0,0,0,0,0,0,0,0,0,0;
%     0,0,0,0,0,0,0,0,0,0;
%     0,0,0,0,0,0,0,0,0,0;
%     0,0,0,0,0,0,0,0,0,0;
%     0,0,0,0,0,0,0,0,0,0;];

%MU=[1/0.2,1/0.150,1/0.080,1/0.150,1/0.200]';
% MU=1./([flip(diff(flip(RTm(1,:)))),RTm(1,end)]/1000);

% NC=ones(size(RTm));
% NC(:,1)=1000.0;
% NC(:,2)=8.0;
% NC(:,3)=4.0;

Tmax=NC(1,:).* MU';
U=Tm./Tmax;

CIdx=sum(sum(RTm,2)~=0);
RTm=RTm/1000;

labels={};
for i=1:size(ms,1)
    labels{i}=ms(i,:);
end

RTl=zeros(CIdx,size(RTm,2));
Tl=zeros(CIdx,size(RTm,2));
for i=1:CIdx
    %Kpi=lineQN([Cli(i)],P,MU,NC(i,:));
    disp(Cli(1,i))
    
    X0=[Cli(1,i),zeros(1,size(P,2)-1)];
    [t,y,T,RT]=QN_ODE(X0,NC(i,:),P,MU,inf);
    
    RTl(i,:)=solveRT2(P2,RT');
    Tl(i,:)=T;
end

for cmp=1:size(RTm,2)
    figure
    title(sprintf("Response Time Dynamics of %s",labels{cmp}))
    hold on
    box on
    grid on
    
    L=RTm(1:CIdx,cmp)-rtCI(1:CIdx,cmp);
    H=RTm(1:CIdx,cmp)+rtCI(1:CIdx,cmp);
    %
    plot(H,"-.") %H
    plot(L,"-.") %L
    %
    %     x2 = [Cli'; flipud(Cli')];
    %     x3=  [linspace(0,size(Cli,2),size(Cli,2))';flipud(linspace(0,size(Cli,2),size(Cli,2))')];
    %     fill(x3, [L; flipud(H)], 'g', 'FaceAlpha',0.5);
    
    stem(RTm(1:CIdx,cmp),"linewidth",1.1,'LineStyle','none')
    stem(RTl(:,cmp),"-.","linewidth",1.3,'LineStyle','none')
    %stem(RTlqn_Ode(cmp,1:CIdx)',"--","linewidth",1.3,'LineStyle','none')
    legend(["RT_m","RT_p"])
end
%
%
for cmp=1:size(Tm,2)
    figure
    title(sprintf("Troughput Dynamics of MS %s",labels{cmp}))
    hold on
    box on
    grid on
    stem(Tm(1:CIdx,cmp),"linewidth",1.1,'LineStyle','none')
    stem(Tl(1:CIdx,cmp),"-.","linewidth",1.3,'LineStyle','none')
    legend(["T_m","T_p"])
end

figure
boxplot(abs(RTm(1:CIdx,:)-RTl)*100./RTm(1:CIdx,:),'Labels',labels)
title("Relative Prediction Error (Response Time)")
box on
grid on
ylabel("(%)")

figure
boxplot(abs(Tm(1:CIdx,:)-Tl)*100./Tm(1:CIdx,:),'Labels',labels)
title("Relative Prediction Error (Throughput)")
box on
grid on
ylabel("(%)")

testClient(RTm,P2)

function [RT]=testClient(RTm,P2)
    RT=[];
    for i =1:size(RTm,1)
        RT=[RT;RTm(i,1)-P2(1,:)*(RTm(i,:)')];
    end
end


