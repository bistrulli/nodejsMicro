function [t,y,Ts,RT]=QN_ODE(X0,S,P,MU,TF)
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

[jump,propensities_2state]=genStoich(P);
pfun = eval(propensities_2state);
T = @(X)pfun(X,p);

opts = odeset('Events',@(t,y)eventfun(t,y,jump,T));
[t,y]=ode45(@(t,y) jump'*T(y),[0,1000], X0,opts);

Ts=T(y(end,:));
Ts=sum(reshape(Ts',size(P,1)-1,size(P,1))',2);

RT=y(end,:)./(Ts');

end

% Propensity rate vector (CTMC)
% function Rate = propensities_2state(x, p)
% Rate = [
%         p.P(1,2)*p.MU(1)*min(x(1),p.S(1));
%      	p.P(1,3)*p.MU(1)*min(x(1),p.S(1));
%      	p.P(2,1)*p.MU(2)*min(x(2),p.S(2));
%      	p.P(2,3)*p.MU(2)*min(x(2),p.S(2));
%      	p.P(3,1)*p.MU(3)*min(x(3),p.S(3));
%      	p.P(3,2)*p.MU(3)*min(x(3),p.S(3));
%      ];
% Rate(isnan(Rate))=0;
% end

function [x,isterm,dir] = eventfun(t,y,jump,T)    
    dy = jump'*T(y);
    x = norm(dy) - 1e-20;
    %x=max(abs(dy)) - 1e-20;
    isterm = 1;
    dir = 0;
end