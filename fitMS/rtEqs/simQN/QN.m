function X=QN(X0,S,P,MU,TF,rep,dt)
import Gillespie.*

X0=double(X0);
S=double(S);
P=double(P);
MU=double(MU);

if(iscolumn(X0))
    X0=X0';
end
if(iscolumn(S))
    S=S';
end
if(iscolumn(MU))
    MU=MU';
end

p.MU=MU;
p.S=S;
p.P=P;

[stoich_matrix,propensities_2state]=genStoich(P);

tspan = [0, TF];
pfun = eval(propensities_2state);

X=zeros(length(X0),ceil(TF/dt)+1,rep);
for i=1:rep
    [t,x] = directMethod(stoich_matrix, pfun, tspan, X0, p);
    tsin = timeseries(x,t);
    tsout = resample(tsin,linspace(0,TF,ceil(TF/dt)+1),'zoh');
    X(:,:,i)=tsout.Data';
end

end

