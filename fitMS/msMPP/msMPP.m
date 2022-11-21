function X = msMPP(X0,MU,NC,TF,rep,dt)
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
% if(iscolumn(NT))
%     NT = NT';
% end
if(iscolumn(NC))
    NC = NC';
end

p.MU = MU; 
p.NC = NC;
p.delta = 10^5; % context switch rate (super fast)

%states name
%X(1)=X0;
%X(2)=X1;
%X(3)=X1_2;
%X(4)=X1_E;
%X(5)=X2;
%X(6)=X2_E;
%X(7)=X1_C;
%X(8)=X2_C;


% Jump matrix
stoich_matrix=[-1,  +1,  +0,  +0,  +0,  +0,  +0,  +0; 
               +0,  -1,  +1,  +1,  +1,  +0,  +0,  +0;
               +0,  +0,  +0,  -1,  +0,  +0,  +1,  +0;
               +0,  +0,  +0,  +0,  -1,  +1,  +0,  +0;
               +0,  +0,  +0,  +0,  +0,  -1,  +0,  +1;
               +1,  +0,  -1,  +0,  +0,  +0,  -1,  -1;];
    
tspan = [0, TF];
pfun = @propensities_2state;
 
X = zeros(length(X0), ceil(TF/dt) + 1, rep);
for i = 1:rep
    [t, x] = directMethod(stoich_matrix, pfun, tspan, X0, p);
    tsin = timeseries(x,t);
    tsout = resample(tsin, linspace(0, TF, ceil(TF/dt)+1), 'zoh');
    X(:, :, i) = tsout.Data';
end

end

% Propensity rate vector (CTMC)
function Rate = propensities_2state(X, p)
    Rate = [p.MU(1)*X(1);
            p.delta*X(2);
            p.MU(4)*min(X(4),p.NC(1));
            p.delta*X(5);
            p.MU(6)*min(X(6),p.NC(2));
            p.delta*min(X(7),X(8));
    		];
    Rate(isnan(Rate))=0;
end