clear

% ctrlMU=readmatrix("../data/ICDCS/ctrl/step_ctrl_fast/ctrldata.csv");
% mudata=readData("../data/ICDCS/ctrl/step_ctrl_fast/*.csv");

ctrlMU2=readmatrix("../data/ICDCS/ctrl/step_ctrl_gns2/ctrldata.csv");
mudata2=readData("../data/ICDCS/ctrl/step_ctrl_gns2/*.csv");

ctrlMAX=readmatrix("../data/ICDCS/validation/step_gns/ctrldata.csv");
maxdata=readData("../data/ICDCS/validation/step_gns/*.csv");

Tmax = smoothdata(maxdata(1).tr,'movmean',3);
%Tctrl = smoothdata(mudata(1).tr,'movmean',1);
Tctrl2 = smoothdata(mudata2(end).tr,'movmean',3);

figure
hold on
stairs(Tmax)
stairs(ctrlMU2(:,2)*0.77)
%stairs(Tctrl)
stairs(Tctrl2)
legend("Ground thruth","muOpt")

% figure
% hold on
% stairs(sum(ctrlMU2(:,3:end),2))
% 
% s=min(size(mudata2(end).rt,1),size(maxdata(end).rt,1));
% x = [mudata2(end).rt(1:s),maxdata(end).rt(1:s)];
% g = [ones(s,1); 2*ones(s,1);];
% figure
% boxplot(x,g)