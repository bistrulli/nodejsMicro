clear 

NT=[inf,inf,inf];
NC=[inf,3,3];
MU=zeros(1,7);
MU([7,6,5])=[80,5,30];
X0=zeros(1,7);

rep=1;
dt=0.1;
TF=100000;

Cli=1:20;

%states name
%X(1)=XBrowse_2Address;
%X(2)=XAddress_a;
%X(3)=XAddress_2Home;
%X(4)=XHome_a;
%X(5)=XHome_e;
%X(6)=XAddress_e;
%X(7)=XBrowse_browse;

e=zeros(size(Cli,2),3);
for i=1:size(Cli,2)
    
    X0(end)=Cli(i);
    
    X = lqn(X0,MU,NT,NC,TF,rep,dt)';
    Xm=cumsum(X)./linspace(1,size(X,1),size(X,1))';
    xtime=linspace(0,TF,round(TF/dt)+1);

    [t,y]=lqnOde(X0,MU,NT,NC,[0,inf]);

    % figure
    % hold on
    % plot(t,y(:,[5,6,7]))
    % plot(xtime,Xm(:,[5,6,7]))

    e(i,:)=abs(Xm(end,[5,6,7])-y(end,[5,6,7]))*100./Xm(end,[5,6,7]);
    Xm(end,[5,6,7])
    y(end,[5,6,7])
end