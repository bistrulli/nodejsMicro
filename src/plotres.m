clear

ctrlMU=readmatrix("../data/ICDCS/ctrl/step_ctrl/ctrldata.csv");
mudata=readData("../data/ICDCS/ctrl/step_ctrl/*.csv");

ctrlMAX=readmatrix("../data/ICDCS/validation/step/ctrldata.csv");
maxdata=readData("../data/ICDCS/validation/step/*.csv");


Tmax = smoothdata(maxdata(end).tr,'movmean',10);
Tctrl = smoothdata(mudata(end).tr,'movmean',10);

figure
hold on
stairs(Tmax)
stairs(Tctrl)
legend("Ground thruth","muOpt")