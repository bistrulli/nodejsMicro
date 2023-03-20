function obj = computObj(tr,core,w)
maxcpu=15*9;
maxT=max(tr);

obj=1/2*(tr./maxT)-1/2*(core/maxcpu);
%obj=(core/maxcpu);
end