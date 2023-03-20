clear

%exps=["step_slow","sin","step"];
exps=["step"]
% exps=["tweeter_7_8"];

for ex=1:length(exps)

lim=[0,2000];

ctrlGA=zeros(2000,11,30);
ctrlMU=zeros(2000,11,15);
gaT=zeros(size(ctrlGA,1),size(ctrlGA,3));
muT=zeros(size(ctrlMU,1),size(ctrlMU,3));
gadata=[];
mudata=[];
valdata=[];

valT=[];
gaRT=[];
muRT=[];
valRT=[];

fontSize=52;
expWork=exps(1,ex);
expnameMu=sprintf("julia_%s",expWork);
expnameAtom=sprintf("atom_%s",expWork);

gaObj=zeros(size(ctrlGA,1),size(ctrlGA,3));
muObj=zeros(size(ctrlMU,1),size(ctrlMU,3));

%load ga data
for i=1:size(ctrlGA,3)
    ctrlGA(:,:,i)=readmatrix(sprintf("../data/revision2/ctrl/%s_%d/ctrldata.csv",expnameAtom,i-1));
    gadata=[gadata;readData(sprintf("../data/revision2/ctrl/%s_%d/*.csv",expnameAtom,i-1))];
    
    gaRT=[gaRT;gadata(end).rt];
    %gaT=[gaT;gadata(end).tr'];
    gaT(:,i)=gadata(end).tr(1:size(ctrlGA,1));

    nanCountGA=sum(isnan(ctrlGA(:,3:end,i)));
    ctrlGA(:,3:end,i)=fillmissing(ctrlGA(:,3:end,i),'constant',ctrlGA(nanCountGA+1:nanCountGA+1,3:end,i));
   
    gaObj(:,i)=computObj(gaT(:,i), sum(ctrlGA(:,3:end,i),2),ctrlGA(:,2,i));
end

%compute CI for gacontrol
ctrlGACI=zeros(size(ctrlGA,1),2);
for i=1:size(ctrlGA,1)
    datai=squeeze(sum(ctrlGA(i,3:end,:),2));
    ctrlGACI(i,:) = getCI(datai);
end

%compute CI for gaT
gaTCI=zeros(size(gaT,1),2);
for i=1:size(ctrlGA,1)
    gaTCI(i,:) = getCI(gaT(i,:));
end


%load muOpt data
for i=1:size(ctrlMU,3)
    ctrlMU(:,:,i)=readmatrix(sprintf("../data/revision2/ctrl/%s_%d/ctrldata.csv",expnameMu,i-1));
    mudata=[mudata;readData(sprintf("../data/revision2/ctrl/%s_%d/*.csv",expnameMu,i-1))];
    
    muRT=[muRT;mudata(end).rt];
    %muT=[muT;mudata(end).tr'];
    muT(:,i)=mudata(end).tr(1:size(ctrlMU,1));
   
    nanCountMu=sum(isnan(ctrlMU(:,3:end,i)));
    ctrlMU(:,3:end,i)=fillmissing(ctrlMU(:,3:end,i),'constant',0);

    muObj(:,i)=computObj(muT(:,i), sum(ctrlMU(:,3:end,i),2),ctrlMU(:,2,i));
end

%compute CI for mucontrol
ctrlMUCI=zeros(size(ctrlMU,1),2);
for i=1:size(ctrlMU,1)
    datai=squeeze(sum(ctrlMU(i,3:end,:),2));
    ctrlMUCI(i,:) = getCI(datai);
end

%load validation data
for i=1:0
    ctrlVal(:,:,i)=readmatrix(sprintf("../data/revision2/ctrl/validation_const50_%d/ctrldata.csv",i-1));
    valdata=[mudata;readData(sprintf("../data/revision2/ctrl/validation_const50_%d/*.csv",i-1))];
    
    valRT=[muRT;mudata(end).rt];
    valT=[muT;mudata(end).tr'];
   
%     nanCountVal=sum(isnan(ctrlVal(:,3:end,i)));
%     ctrlVal(:,3:end,i)=fillmissing(ctrlVal(:,3:end,i),'constant',ctrlVal(nanCountVal+1:nanCountVal+1,3:end,i));
    ctrlVal(:,3:end,i)=ones(size(ctrlVal,1),9)*150;
end


%load 1_client data
% ctrlMAX=readmatrix("../data/ICDCS/validation/1_client_gns/ctrldata.csv");
% maxdata=readData("../data/ICDCS/validation/1_client_gns/*.csv");

mGA=mean(ctrlGA(:,3:end,:),3);
mMU=mean(ctrlMU(:,3:end,:),3);
% valCtrl=mean(ctrlVal(:,3:end,:),3);


%users figure
figure('units','normalized','outerposition',[0 0 1 1])
stairs(ctrlMU(:,2,1),"LineWidth",2.5);
ylim([10,62])
box on
grid on
ax = gca;
ax.FontSize = fontSize;
xlabel("Time(s)")
ylabel("#Users")
legend("Users","Location","southeast")
axis tight
xlim(lim)
exportgraphics(gca,sprintf("/Users/emilio-imt/git/muOptPaper/figures/acmeair/%s_users.pdf",expWork));
close()


figure('units','normalized','position',[0 0 1 1])
hold on
box on
grid on
hold on
stairs(sum(mMU,2),"LineWidth",2.5,"Color",[0.00,0.45,0.74]);
stairs(sum(mGA,2),"LineWidth",2.5,"Color",[0.85,0.33,0.10]);
stairs(ctrlMUCI(1:end,:),"-.","Color",[0.00,0.45,0.74])
stairs(ctrlGACI(1:end,:),"-.","Color",[0.85,0.33,0.10])
ax = gca;
ax.FontSize = fontSize;
xlabel("Time(s)")
ylabel("#Cores")
legend("\muOpt","ATOM","Location","southeast")
xlim(lim)
exportgraphics(gca,sprintf("/Users/emilio-imt/git/muOptPaper/figures/acmeair/%s_cores.pdf",expWork));
close()

% figure('units','normalized','outerposition',[0 0 1 1])
% hold on
% box on
% grid on
% hold on
% stairs(ctrlMU(:,2,1),"LineWidth",1.5);
% ax = gca;
% ax.FontSize = 24;
% exportgraphics(gca,"/Users/emilio-imt/Desktop/users.pdf")
% close()
%stairs(ctrlGA(:,2))
%stairs(sum(valCtrl,2));



% Tmax = smoothdata(maxdata(1).tr,'movmean',3);
%Tctrl = smoothdata(mudata(end).tr,'movmean',3);
%Tctrlga = smoothdata(gadata(end).tr,'movmean',3);

%throughput
figure('units','normalized','position',[0 0 1 1])
stairs(smoothdata(mean(muT,2),'movmean',3),"LineWidth",2.5);
hold on
stairs(smoothdata(mean(gaT,2),'movmean',3),"LineWidth",2.5,"Color",[0.85,0.33,0.10]);

stairs(smoothdata(gaTCI(:,1),'movmean',3),"-.","Color",[0.85,0.33,0.10],"LineWidth",0.001);
stairs(smoothdata(gaTCI(:,2),'movmean',3),"-.","Color",[0.85,0.33,0.10],"LineWidth",0.001);

grid on;
box on;
legend("\muOpt","ATOM","Location","southeast")
ax = gca;
ax.FontSize = fontSize;
ylabel("Troughput(req/s)")
xlabel("Time(s)")
xlim(lim)
exportgraphics(gca,sprintf("/Users/emilio-imt/git/muOptPaper/figures/acmeair/%s_throughput_t.pdf",expWork));
close()

totMUT=cumsum(mean(muT,2));
totGAT=cumsum(mean(gaT,2));

% figure('units','normalized','outerposition',[0 0 1 1]) 
% hold on
% grid on;
% box on;
% stairs(cumsum(mean(muT,2)),"LineWidth",2.5)
% stairs(cumsum(mean(gaT,2)),"LineWidth",2.5)
% legend("\muOpt","ATOM")
% ax = gca;
% ax.FontSize = fontSize;
% ylabel("CumTroughput(req/s)")
% xlabel("Time(s)")
% axis tight
% exportgraphics(gca,sprintf("/Users/emilio-imt/git/muOptPaper/figures/acmeair/%s_throughput_cum.pdf",expWork));
% close()

% figure
% hold on
% stairs(Tmax)
% stairs(ctrlMAX(:,2)*0.66)
% stairs(Tctrl)
% stairs(Tctrlga)
% legend("muOpt","muGA")

% figure
% hold on
% stairs(sum(ctrlMU(:,3:end),2))
% stairs(sum(ctrlGA(:,3:end),2))

% s=min([size(muRT,1),size(gaRT,1)]);
% x = [muRT(1:s),gaRT(1:s)];
% g = [ones(s,1); 2*ones(s,1)];
% figure
% boxplot(x,g)

% figure('units','normalized','outerposition',[0 0 1 1])
% hold on
% grid on;
% box on;
% [fmu,x1]=ecdf(muRT);
% [fga,x2]=ecdf(gaRT);
% plot(x1,fmu,"LineWidth",2.5);
% plot(x2,fga,"LineWidth",2.5);
% legend("\muOpt","ATOM")
% xlabel("Time(s)")
% ylabel("F(x)")
% ax = gca;
% ax.FontSize = fontSize;
% exportgraphics(gca,sprintf("/Users/emilio-imt/git/muOptPaper/figures/acmeair/%s_CDF.pdf",expWork));
% close()


for i=1:min(size(ctrlGA,3),size(ctrlMU,3))
    deltaS(i)=(-trapz(sum(ctrlGA(:,3:end,i),2))+trapz(sum(ctrlMU(:,3:end,i),2)))*100/trapz(sum(ctrlMU(:,3:end,i),2));
    deltaT(i)=mean(muT(:,i)-gaT(:,i))*100/mean(muT(:,i));
end

% figure('units','normalized','outerposition',[0 0 0.5 0.5])
figure
set(gcf,'units','normalized',"position",[0 0 0.5 1]);
hold on
%somedata=[(totMUT(end)-totGAT(end))*100/totMUT(end),(-trapz(sum(mGA,2))+trapz(sum(mMU,2)))*100/trapz(sum(mMU,2))];
somedata=[mean(deltaT),mean(deltaS)]
%somenames={"$\Delta\mathcal{T}$",'$\Delta\mathcal{S}$'};
somenames={" "," "};
% set(groot,'defaultAxesTickLabelInterpreter','latex');
% set(groot,'defaulttextinterpreter','latex');
% set(groot,'defaultLegendInterpreter','latex');
h=bar([1,2],somedata);
h.FaceColor="flat";
h.CData(1,:)=[241 197 58]/255;
grid on;
box on;
set(gca,'xticklabel',somenames)
ylabel("%")
% ylim([0,1])
ax = gca;
ax.FontSize = fontSize;
xlim([0.5,2.5])
xh = get(gca,'xlabel');
xh.Color=[1,1,1];
xlabel("time");

CIdt=getCI(deltaT)-mean(deltaT);
CIds=getCI(deltaS)-mean(deltaS);
errorbar([1,2],[mean(deltaT),mean(deltaS)],[CIdt(1),CIds(1)],[CIdt(2),CIds(2)],'x',"LineWidth",2,"Color","red");
exportgraphics(gca,sprintf("/Users/emilio-imt/git/muOptPaper/figures/acmeair/%s_stat.pdf",expWork));
close()


figure('units','normalized','position',[0 0 1 1])
stairs(smoothdata(mean(muObj,2),'movmean',3),"LineWidth",2.5)
hold on
stairs(smoothdata(mean(gaObj,2),'movmean',3),"--","LineWidth",2.5)

grid on;
box on;
legend("\muOpt","ATOM","Location","southeast")
ax = gca;
ax.FontSize = fontSize;
%ylabel("Obj")
xlabel("Time(s)")
xlim(lim)
exportgraphics(gca,sprintf("/Users/emilio-imt/git/muOptPaper/figures/acmeair/%s_obj.pdf",expWork));
close()


end

