function [t,y] = lqnOde(X0,MU,NT,NC,TF)
import Gillespie.*

% Make sure vector components are doubles
X0 = double(X0);
MU = double(MU);

% Make sure all vectors are row vectors
if(iscolumn(X0))
    X0 = X0';
end
if(iscolumn(MU))
    MU = MU';
end
if(iscolumn(NT))
    NT = NT';
end
if(iscolumn(NT))
    NC = NC';
end

p.MU = MU;
p.NT = NT;
p.NC = NC;
p.delta = 10^5; % context switch rate (super fast)

%states name
%X(1)=XBrowse_2Address;
%X(2)=XAddress_a;
%X(3)=XAddress_2Home;
%X(4)=XHome_a;
%X(5)=XHome_e;
%X(6)=XAddress_e;
%X(7)=XBrowse_browse;


%task ordering
%1=Client;
%2=Router;
%3=Front_end;


% Jump matrix
jump=[+1,  +1,  +0,  +0,  +0,  +0,  -1;
    +0,  -1,  +1,  +1,  +0,  +0,  +0;
    +0,  +0,  +0,  -1,  +1,  +0,  +0;
    +0,  +0,  -1,  +0,  -1,  +1,  +0;
    -1,  +0,  +0,  +0,  +0,  -1,  +1;
    ];

pfun = @propensities_2state;

T = @(X)pfun(X,p);

opts = odeset('Events',@(t,y)eventfun(t,y,jump,T));
[t,y]=ode15s(@(t,y) jump'*T(y),TF, X0,opts);

end

% Propensity rate vector (CTMC)
function Rate = propensities_2state(X, p)
Rate = [p.MU(7)*X(7);
    X(2)/(X(2))*p.delta*min(X(2),p.NT(2)-(X(3)+X(6)));
    X(4)/(X(4))*p.delta*min(X(4),p.NT(3)-(X(5)));
    X(3)/(X(3))*X(5)/(X(5))*min(X(5),p.NC(3))*p.MU(5);
    X(1)/(X(1))*X(6)/(X(6))*min(X(6),p.NC(2))*p.MU(6);
    ];
Rate(isnan(Rate))=0;
end


function [x,isterm,dir] = eventfun(t,y,jump,T)
dy = jump'*T(y);
x = norm(dy) - 1e-5;
%x=max(abs(dy)) - 1e-5;
isterm = 1;
dir = 0;
end