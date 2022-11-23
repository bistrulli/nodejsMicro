server = "localhost";
port = 27017;
dbname = "sys";
conn = mongoc(server,port,dbname);

if(~isopen(conn))
    error("error whilt connecting to mongodb")
end

%inizializzo la simulazione
%devo recuperare il numero di client inizili dal db
%devo impostare le configurazioni del numero di core iniziali su redis
%perchè è li le che verranno lette
updateShare("MSauth",15);
initSim(conn)

% lancio il sistema
startSystem(conn)

%ora posso comunicare con i diversi microservizi aggiornando il campo hw
%del rispettivo document nella collection ms del database sys
disp("doing things")
disp(datetime)
pause(60*3)
%vario i core del microservizio auth per farlo diventare bottleneck
updateShare("MSauth",1);
disp(datetime)
pause(60*3)
updateShare("MSauth",2);
disp(datetime)
pause(60*3)

%stoppo il sistrema settamndo a 1 il campo toStop
stopStystem(conn);

msFiles=dir("../data/ICDCS/*.csv");
msData=struct("name",[],"rt",[],"tr",[]);
for i=1:size(msFiles,1)
    msData(i).name=msFiles(i).name;
    msData(i).rt=getMSRt(sprintf("%s/%s",msFiles(i).folder,msFiles(i).name));
    msData(i).tr=getMSTr(sprintf("%s/%s",msFiles(i).folder,msFiles(i).name));
end


%per visualizzare i risultati importo i csv che sono stati esportati dal
%sisrtema
close(conn)

function initSim(conn)
collection = "sim";
try
    dropCollection(conn,collection)
catch
end
createCollection(conn,collection)
simDoc.started=0;
simDoc.toStop=0;
insert(conn,collection,simDoc);
end

function stopStystem(conn)
disp("stopping system")
findquery = "{""started"":1}";
updatequery = "{""$set"":{""toStop"":1}}";
n = update(conn,"sim",findquery,updatequery);

isStopped=false;
while(~isStopped)
    try
        simDoc = find(conn,"sim");
    catch
        isStopped=true;
    end
end
disp("system stopped")
end

function startSystem(conn)
[status,cmdout] = system("python3 acmeAir_ICDCS.py &");
%aspetto che il sistema sia partito completamnte
simDoc = find(conn,"sim");
while(simDoc.started~=1)
    disp("waiting system to start")
    pause(0.5)
    try
        simDoc = find(conn,"sim");
    catch
    end
end
disp("system started")
end

function rt=getMSRt(dataPath)
cmp_evt = readmatrix(dataPath);
rt=(cmp_evt(:,2)-cmp_evt(:,1))/10^3;
end

function tr=getMSTr(dataPath)
cmp_evt = readmatrix(dataPath);
kidx=1;
tcmp=0;
tr=[];
i=1;
while(i<=size(cmp_evt,1))
    if((kidx-1)<=(cmp_evt(i,2)-min(cmp_evt(:,2)))/10^3 && (cmp_evt(i,2)-min(cmp_evt(:,2)))/10^3<=(kidx))
        tcmp=tcmp+1;
        i=i+1;
    else
        tr=[tr,tcmp];
        tcmp=0;
        kidx=kidx+1;
    end
end
end

function updateShare(msname,share)
fprintf("update share of %s to %.3f",msname,share);
%     findquery = sprintf("{""name"":""%s""}",msname);
%     updatequery = sprintf("{""$set"":{""hw"":%.3f}}",max(0,share));
%     update(conn,"ms",findquery,updatequery);

r = Redis("localhost",6379);
r.set(sprintf("%s_hw",msname),sprintf("%.3f",share));

%lo lasico solo come esempio per fare una query
%find(conn,"ms",Query=mongoquery);
end
