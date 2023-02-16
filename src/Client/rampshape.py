from Client import loadShape

class RampShape(loadShape):
    def __init__(self, maxt,sys,dry=False,dbHost="127.0.0.1",datadir=None,slope, steady, initial=1, rampstart=0):
        super().__init__(maxt,sys,dry,dbHost,datadir)
        
        self.slope = slope
        self.steady = steady
        self.initial = initial
        self.rampstart = rampstart

    def gen(self):
        if self.t < self.rampstart:
            return self.initial
        if self.t < self.steady:
            return self.initial+self.slope*(self.t-self.rampstart)
        else:
            return self.initial+(self.steady-self.rampstart)*self.slope
