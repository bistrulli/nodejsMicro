clear

ctrlMU=readmatrix("../data/revision2/ctrl/muopt_const50/ctrldata.csv");
mudata=readData("../data/revision2/ctrl/muopt_const50/*.csv");

ctrlGA=readmatrix("../data/revision2/ctrl/atom_const50_1/ctrldata.csv");
gadata=readData("../data/revision2/ctrl/atom_const50_1/*.csv");

nanCountGA=sum(isnan(ctrlGA(:,3:end)));
nanCountMu=sum(isnan(ctrlMU(:,3:end)));

ctrlGA=fillmissing(ctrlGA(:,3:end),'constant',ctrlGA(nanCountGA+1:nanCountGA+1,3:end));
ctrlMU=fillmissing(ctrlMU(:,3:end),'constant',ctrlMU(nanCountMu+1:nanCountMu+1,3:end));

% ctrlMAX=readmatrix("../data/ICDCS/validation/step_gns_150/ctrldata.csv");
% maxdata=readData("../data/ICDCS/validation/step_gns_150/*.csv");

% Tmax = smoothdata(maxdata(1).tr,'movmean',3);
Tctrl = smoothdata(mudata(1).tr,'movmean',3);
Tctrlga = smoothdata(gadata(end).tr,'movmean',3);

figure
hold on
% stairs(Tmax)
% stairs(ctrlMAX(:,2)*0.66)
stairs(Tctrl)
stairs(Tctrlga)
legend("muOpt","muGA")

figure
hold on
stairs(sum(ctrlMU(:,3:end),2))
stairs(sum(ctrlGA(:,3:end),2))

s=min([size(mudata(end).rt,1),size(gadata(end).rt,1)]);
x = [mudata(end).rt(1:s),gadata(end).rt(1:s)];
g = [ones(s,1); 2*ones(s,1);];
figure
boxplot(x,g)

figure
ecdf(mudata(end).rt)
hold on
ecdf(gadata(end).rt)
legend("\mu_{opt}","GA")


(trapz(sum(ctrlGA,2))-trapz(sum(ctrlMU,2)))*100/trapz(sum(ctrlMU,2))

