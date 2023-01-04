% clear

msdata=readData("../data/ICDCS/ctrl_2/*.csv");

figure
hold on
plot(cumsum(msdata(end).rt)'./linspace(1,size(cumsum(msdata(10).rt),1),size(cumsum(msdata(10).rt),1)))
% plot(cumsum(msdata2(10).rt)'./linspace(1,size(cumsum(msdata2(10).rt),1),size(cumsum(msdata2(10).rt),1)))
% plot(cumsum(msdata3(10).rt)'./linspace(1,size(cumsum(msdata3(10).rt),1),size(cumsum(msdata3(10).rt),1)))
% legend("ctrl","noctrl","delayed")