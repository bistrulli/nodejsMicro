clear

% ctrlMU=readmatrix("../data/ICDCS/ctrl/step_gns_150/ctrldata.csv");
% mudata=readData("../data/ICDCS/ctrl/step_gns_150/*.csv");

ctrlGA=readmatrix("../data/revision2/ctrl/atom_const50/ctrldata.csv");
gadata=readData("../data/revision2/ctrl/atom_const50/*.csv");

% ctrlMAX=readmatrix("../data/ICDCS/validation/step_gns_150/ctrldata.csv");
% maxdata=readData("../data/ICDCS/validation/step_gns_150/*.csv");

% Tmax = smoothdata(maxdata(1).tr,'movmean',3);
% Tctrl = smoothdata(mudata(1).tr,'movmean',3);
Tctrlga = smoothdata(gadata(end).tr,'movmean',3);

figure
hold on
% stairs(Tmax)
% stairs(ctrlMAX(:,2)*0.66)
% stairs(Tctrl)
stairs(Tctrlga)
legend("Ground thruth","muOpt","muGA")

figure
hold on
% stairs(sum(ctrlMU(:,3:end),2))
stairs(sum(ctrlGA(:,3:end),2))

% s=min([size(mudata(end).rt,1),size(maxdata(end).rt,1),size(gadata(end).rt,1)]);
% x = [mudata(end).rt(1:s),maxdata(end).rt(1:s),gadata(end).rt(1:s)];
% g = [ones(s,1); 2*ones(s,1);3*ones(s,1)];
% figure
% boxplot(x,g)
% 
% figure
% ecdf(mudata(end).rt)
% hold on
% ecdf(maxdata(end).rt)
% ecdf(gadata(end).rt)
% legend("\mu_{opt}","MAX","GA")
% 
% (trapz(sum(fillmissing(ctrlGA(:,3:end),'constant',300),2))-trapz(sum(fillmissing(ctrlMU(:,3:end),'constant',300),2)))*100/trapz(sum(fillmissing(ctrlMU(:,3:end),'constant',300),2))

