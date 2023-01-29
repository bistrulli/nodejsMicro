clear

ctrlMU=readmatrix("../data/ICDCS/ctrl/step_ctrl_fast/ctrldata.csv");
mudata=readData("../data/ICDCS/ctrl/step_ctrl_fast/*.csv");

% ctrlMU2=readmatrix("../data/ICDCS/ctrl/step_ctrl7/ctrldata.csv");
% mudata2=readData("../data/ICDCS/ctrl/step_ctrl7/*.csv");

ctrlMAX=readmatrix("../data/ICDCS/validation/step_fast/ctrldata.csv");
maxdata=readData("../data/ICDCS/validation/step_fast/*.csv");


Tmax = smoothdata(maxdata(1).tr,'movmean',10);
Tctrl = smoothdata(mudata(1).tr,'movmean',10);
% Tctrl2 = smoothdata(mudata2(end).tr,'movmean',3);

figure
hold on
stairs(Tmax)
stairs(Tctrl)
% stairs(Tctrl2)
legend("Ground thruth","muOpt","muOpt2")