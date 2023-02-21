clear

ctrlGA=zeros(2000,11,15);
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

expnameMu="julia_sin";
expnameAtom="atom_sin";

%load ga data
for i=1:size(ctrlGA,3)
    ctrlGA(:,:,i)=readmatrix(sprintf("../data/revision2/ctrl/%s_%d/ctrldata.csv",expnameAtom,i-1));
    gadata=[gadata;readData(sprintf("../data/revision2/ctrl/%s_%d/*.csv",expnameAtom,i-1))];
    
    gaRT=[gaRT;gadata(end).rt];
    %gaT=[gaT;gadata(end).tr'];
    gaT(:,i)=gadata(end).tr(1:size(ctrlGA,1));

    nanCountGA=sum(isnan(ctrlGA(:,3:end,i)));
    ctrlGA(:,3:end,i)=fillmissing(ctrlGA(:,3:end,i),'constant',ctrlGA(nanCountGA+1:nanCountGA+1,3:end,i));
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




legend("Users")
ax = gca;
ax.FontSize = 24;
ylim([0,65])
stairs(ctrlMU(:,2,1))


figure('units','normalized','outerposition',[0 0 1 1])
hold on
box on
grid on
hold on
stairs(sum(mGA,2),"LineWidth",1.5);
stairs(sum(mMU,2),"LineWidth",1.5);
ax = gca;
ax.FontSize = 24;
exportgraphics(gca,"/Users/emilio-imt/Desktop/ctrlCore.pdf")
close()

figure('units','normalized','outerposition',[0 0 1 1])
hold on
box on
grid on
hold on
stairs(ctrlMU(:,2,1),"LineWidth",1.5);
ax = gca;
ax.FontSize = 24;
exportgraphics(gca,"/Users/emilio-imt/Desktop/users.pdf")
close()
%stairs(ctrlGA(:,2))
%stairs(sum(valCtrl,2));



% Tmax = smoothdata(maxdata(1).tr,'movmean',3);
%Tctrl = smoothdata(mudata(end).tr,'movmean',3);
%Tctrlga = smoothdata(gadata(end).tr,'movmean',3);

figure
stairs(smoothdata(mean(muT,2),'movmean',1));
hold on
stairs(smoothdata(mean(gaT,2),'movmean',1));
legend("muOpt","muGA")

totMUT=cumsum(mean(muT,2));
totGAT=cumsum(mean(gaT,2));

figure 
hold on
stairs(cumsum(mean(muT,2)))
stairs(cumsum(mean(gaT,2)))

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

s=min([size(muRT,1),size(gaRT,1)]);
x = [muRT(1:s),gaRT(1:s)];
g = [ones(s,1); 2*ones(s,1)];
figure
boxplot(x,g)

figure
hold on
ecdf(muRT)
ecdf(gaRT)
legend("muOpt","muGA")
% ecdf(valRT)


abs(totMUT(end)-totGAT(end))*100/totMUT(end)
(trapz(sum(mGA,2))-trapz(sum(mMU,2)))*100/trapz(sum(mMU,2))

