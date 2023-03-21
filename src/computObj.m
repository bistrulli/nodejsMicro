function obj = computObj(tr,core,w)
maxcpu=20*9;
%maxT=max(tr)
maxT=max(tr);

obj=1/2*(tr./maxT)-1/2*(core/maxcpu);
%obj=(core/maxcpu);
end