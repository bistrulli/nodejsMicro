from Client import loadShape
from numpy.random import default_rng
import numpy as np
from scipy.io import savemat
from scipy.io import loadmat
import os


class StepShape(loadShape):
    def __init__(self, maxt,sys,dry=False,dbHost="127.0.0.1",datadir=None,intervals=None, values=None,shapeData=None):
        super().__init__(maxt,sys,dry,dbHost,datadir)
        
        if(intervals is None and values is None and shapeData is not None):
            absolute_path = os.path.dirname(__file__)
            trace_path = os.path.join(absolute_path, "%s.mat"%(shapeData))
            intervals=loadmat(trace_path)["intervals"][0]
            values=loadmat(trace_path)["values"][0]
        else:
            raise ValueError("at lest one between interval and stepShape should be specified")
        
        assert len(intervals) == len(values)
        self.intervals = intervals
        self.values = values
        self.int_step = 0

    def gen(self):
        
        if self.int_step < len(self.intervals) and self.t == self.intervals[self.int_step]:
            self.int_step += 1
            
        return self.values[self.int_step-1]


if __name__ == '__main__':
    
    import matplotlib.pyplot as plt
    
    rng = default_rng()
    
    maxtime=2000
    Nint=int(maxtime/500.0)
    users=[]
    values=np.random.randint(low=10,high=65,size=Nint, dtype=int)
    #intervals = rng.choice(Nint*2, size=Nint, replace=False)
    intervals=np.linspace(1,maxtime+1,Nint,dtype=int)
    intervals=np.sort(intervals)
    print(intervals)
    print(values)
    
    stepShape=StepShape(maxt=None,sys=None,dry=False,dbHost="127.0.0.1",datadir=None,
                        intervals=intervals,
                        values=values)
    
    for i in range(maxtime):
        stepShape.t=i
        users+=[stepShape.gen()]
        
    plt.step(np.linspace(1,len(users),len(users)),users)
    plt.show()
    
    savemat("stepshape_slow.mat",{"intervals":intervals,"values":values})
    trace=loadmat("stepshape_slow.mat")