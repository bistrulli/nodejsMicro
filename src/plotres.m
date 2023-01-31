clear

% ctrlMU=readmatrix("../data/ICDCS/ctrl/step_ctrl_fast/ctrldata.csv");
% mudata=readData("../data/ICDCS/ctrl/step_ctrl_fast/*.csv");

% ctrlMU2=readmatrix("../data/ICDCS/ctrl/step_ctrl7/ctrldata.csv");
% mudata2=readData("../data/ICDCS/ctrl/step_ctrl7/*.csv");

ctrlMAX=readmatrix("../data/ICDCS/validation/step_gns/ctrldata.csv");
maxdata=readData("../data/ICDCS/validation/step_gns/*.csv");


Tmax = smoothdata(maxdata(1).tr,'movmean',5);
%Tctrl = smoothdata(mudata(1).tr,'movmean',1);
% Tctrl2 = smoothdata(mudata2(end).tr,'movmean',3);

figure
hold on
stairs(Tmax)
stairs(ctrlMAX(:,2)*0.77)
%stairs(Tctrl)
% stairs(Tctrl2)
legend("Ground thruth","muOpt")