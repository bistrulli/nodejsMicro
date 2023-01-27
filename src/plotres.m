clear

ctrlMU=readmatrix("../data/ICDCS/ctrl/step_ctrl/ctrldata.csv");
mudata=readData("../data/ICDCS/ctrl/step_ctrl/*.csv");

ctrlMU2=readmatrix("../data/ICDCS/ctrl/step_ctrl2/ctrldata.csv");
mudata2=readData("../data/ICDCS/ctrl/step_ctrl2/*.csv");

ctrlMAX=readmatrix("../data/ICDCS/validation/step/ctrldata.csv");
maxdata=readData("../data/ICDCS/validation/step/*.csv");


Tmax = smoothdata(maxdata(end).tr,'movmean',10);
Tctrl = smoothdata(mudata(end).tr,'movmean',10);
Tctrl2 = smoothdata(mudata2(end).tr,'movmean',10);

figure
hold on
stairs(Tmax)
stairs(Tctrl)
stairs(Tctrl2)
legend("Ground thruth","muOpt","muOpt2")