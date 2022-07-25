clear
load("/Users/emilio/git/nodejsMicro/data/3tier_test_java_jitless.mat");
load("/Users/emilio/git/MS-App/fitLQN/fromJulia.mat")

P=[0,1,0;
   0,0,1;
   1,0,0;];

P2=[0,1,0;
    0,0,1;
    0,0,0;];

MU=[1/0.1,1/0.12,1/0.1];


CIdx=sum(sum(RTm,2)~=0);
RTm=RTm/1000;

labels={};
for i=1:size(ms,1)
    labels{i}=ms(i,:);
end

RTl=zeros(CIdx,size(RTm,2));
Tl=zeros(CIdx,size(RTm,2));
for i=CIdx:CIdx
    %Kpi=lineQN([Cli(i)],P,MU,NC(i,:));
    
    X0=[Cli(i),zeros(1,size(P,2)-1)];
    [t,y,T,RT]=QN_ODE(X0,NC(i,:),P,MU);
    
    RTl(i,:)=solveRT2(P2,RT');
    Tl(i,:)=T;
end

% for cmp=1:size(RTm,2)
%     figure
%     title(sprintf("Response Time Dynamics of %s",labels{cmp}))
%     hold on
%     box on
%     grid on
%     stem(RTm(1:CIdx,cmp),"linewidth",1.1,'LineStyle','none')
%     stem(RTl(:,cmp),"-.","linewidth",1.3,'LineStyle','none')
%     %stem(RTlqn_Ode(cmp,1:CIdx)',"--","linewidth",1.3,'LineStyle','none')
%     legend(["RT_m","RT_p","RT_ode"])
% end
% 
% 
% for cmp=1:size(Tm,2)
%     figure
%     title(sprintf("Troughput Dynamics of MS %s",labels{cmp}))
%     hold on
%     box on
%     grid on
%     stem(Tm(1:CIdx,cmp),"linewidth",1.1,'LineStyle','none')
%     stem(Tl(1:CIdx,cmp),"-.","linewidth",1.3,'LineStyle','none')
%     legend(["T_m","T_p"])
% end

% figure
% boxplot(abs(RTm(1:CIdx,:)-RTl)*100./RTm(1:CIdx,:),'Labels',labels)
% title("Relative Prediction Error (Response Time)")
% box on
% grid on
% ylabel("(%)")
% 
% figure
% boxplot(abs(Tm(1:CIdx,:)-Tl)*100./Tm(1:CIdx,:),'Labels',labels)
% title("Relative Prediction Error (Throughput)")
% box on
% grid on
% ylabel("(%)")


