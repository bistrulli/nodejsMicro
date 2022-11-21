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
p.Delta=10^8;

%%
%X(1)=X0
%X(2)=X01
%X(3)=X1e
%X(4)=X0t
%X(5)=X01a
%X(6)=X0e
%X(7)=X01f
%X(8)=X0f
%X(9)=X0et

%P(1)=P01
%P(2)=P01A
%P(3)=P0E

%MU(1)=MU0
%MU(2)=MU1

%S(1)=S0
%S(2)=S1

              
stoich_matrix=[ 0,  +1,  +1,  +0,  +0,  +0,  +0,  +0,  +0;
               -1,  -1,  +0,  +0,  +1,  +0,  +0,  +0,  +0;
               -1,  +0,  +0,  +0,  +0,  +1,  +0,  +0,  +0;
               +0,  +0,  +0,  +1,  +0,  -1,  +0,  +0,  +0;
               +0,  +0,  -1,  +0,  +0,  +0,  +1,  +0,  +0;
               +0,  +0,  +0,  +1,  -1,  +0,  -1,  +0,  +0;
               +0,  +0,  +0,  -1,  +0,  +0,  +0,  +1,  +1;
               +1,  +0,  +0,  +0,  +0,  +0,  +0,  -1,  +0;
               ];

tspan = [0, TF];
pfun =@propensities_2state;

X=zeros(length(X0),ceil(TF/dt)+1,rep);
for i=1:rep
    [t,x] = directMethod(stoich_matrix, pfun, tspan, X0, p);
    tsin = timeseries(x,t);
    tsout = resample(tsin,linspace(0,TF,ceil(TF/dt)+1),'zoh');
    X(:,:,i)=tsout.Data';
end

end

function Rate = propensities_2state(X,p)
    Rate = [p.P(1)*p.Delta*X(1);
            p.P(2)*p.Delta*min(X(1),X(2));
            p.P(3)*p.Delta*X(1);
            p.MU(1)*min(X(6),p.S(1));
            p.MU(2)*min(X(3),p.S(2));
            p.Delta*min(X(5),X(7));
            p.Delta*X(4);
            p.Delta*X(8);
            ];
    Rate(isnan(Rate))=0;
end


