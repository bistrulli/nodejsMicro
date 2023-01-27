function msData=readData(dataPath)
msFiles=dir(dataPath);
disp(dataPath)
msData=struct("name",[],"rt",[],"tr",[]);
for i=1:size(msFiles,1)
    
    if(contains(msFiles(i).name,"ctrldata.csv"))
        continue
    end

    msData(i).name=msFiles(i).name;
    disp(msFiles(i).name)
    msData(i).rt=getMSRt(sprintf("%s/%s",msFiles(i).folder,msFiles(i).name));
    msData(i).tr=getMSTr(sprintf("%s/%s",msFiles(i).folder,msFiles(i).name));
end
end