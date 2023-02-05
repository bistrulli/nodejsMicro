clear

ctrlMU=readmatrix("../data/ICDCS/ctrl/step_gns_150/ctrldata.csv");
mudata=readData("../data/ICDCS/ctrl/step_gns_150/*.csv");

% ctrlMU2=readmatrix("../data/ICDCS/ctrl/step_ctrl_gns2/ctrldata.csv");
% mudata2=readData("../data/ICDCS/ctrl/step_ctrl_gns2/*.csv");

ctrlMAX=readmatrix("../data/ICDCS/validation/step_gns_150/ctrldata.csv");
maxdata=readData("../data/ICDCS/validation/step_gns_150/*.csv");

Tmax = smoothdata(maxdata(1).tr,'movmean',3);
Tctrl = smoothdata(mudata(1).tr,'movmean',3);
% Tctrl2 = smoothdata(mudata2(end).tr,'movmean',3);

figure
hold on
stairs(Tmax)
% stairs(ctrlMAX(:,2)*0.66)
stairs(Tctrl)
% stairs(Tctrl2)
legend("Ground thruth","muOpt")

figure
hold on
stairs(ctrlMU(:,3:end))

s=min(size(mudata(end).rt,1),size(maxdata(end).rt,1));
x = [mudata(end).rt(1:s),maxdata(end).rt(1:s)];
g = [ones(s,1); 2*ones(s,1);];
figure
boxplot(x,g)


ecdf(mudata(end).rt)
hold on
ecdf(maxdata(end).rt)
legend("\mu_{opt}","MAX")