clear

ctrlGA=zeros(1200,11,15);
ctrlMU=zeros(1200,11,1);
gadata=[];
mudata=[];
gaT=[];
muT=[];

gaRT=[];
muRT=[];

%load ga data
for i=1:15
    ctrlGA(:,:,i)=readmatrix(sprintf("../data/revision2/ctrl/atom_const150_%d/ctrldata.csv",i-1));
    gadata=[gadata;readData(sprintf("../data/revision2/ctrl/atom_const150_%d/*.csv",i-1))];
    
    gaRT=[gaRT;gadata(end).rt];
    gaT=[gaT;gadata(end).tr'];

    nanCountGA=sum(isnan(ctrlGA(:,3:end,i)));
    ctrlGA(:,3:end,i)=fillmissing(ctrlGA(:,3:end,i),'constant',ctrlGA(nanCountGA+2:nanCountGA+2,3:end,i));
end

%load muOpt data
for i=1:15
    ctrlMU(:,:,i)=readmatrix(sprintf("../data/revision2/ctrl/muopt_const150_%d/ctrldata.csv",i-1));
    mudata=[mudata;readData(sprintf("../data/revision2/ctrl/muopt_const150_%d/*.csv",i-1))];
    
    muRT=[muRT;mudata(end).rt];
    muT=[muT;mudata(end).tr'];
   
    nanCountMu=sum(isnan(ctrlMU(:,3:end,i)));
    ctrlMU(:,3:end,i)=fillmissing(ctrlMU(:,3:end,i),'constant',ctrlMU(nanCountMu+1:nanCountMu+1,3:end,i));
end

%load 1_client data
ctrlMAX=readmatrix("../data/ICDCS/validation/1_client_gns/ctrldata.csv");
maxdata=readData("../data/ICDCS/validation/1_client_gns/*.csv");

mGA=mean(ctrlGA(:,3:end,:),3);
mMU=mean(ctrlMU(:,3:end,:),3);

figure
hold on
stairs(sum(mGA,2));
stairs(sum(mMU,2));



% Tmax = smoothdata(maxdata(1).tr,'movmean',3);
% Tctrl = smoothdata(mudata(1).tr,'movmean',3);
% Tctrlga = smoothdata(gadata(end).tr,'movmean',3);

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
g = [ones(s,1); 2*ones(s,1);];
figure
boxplot(x,g)

figure
hold on
ecdf(muRT)
ecdf(gaRT)



(trapz(sum(mGA,2))-trapz(sum(mMU,2)))*100/trapz(sum(mMU,2))

