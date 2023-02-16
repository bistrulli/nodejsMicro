from Client import loadShape
import math


class SinShape(loadShape):
    def __init__(self, maxt,sys,dry=False,dbHost="127.0.0.1",datadir=None,mod, shift, period=100):
        super().__init__(maxt,sys,dry,dbHost,datadir)
        
        self.mod = mod
        self.shift = shift
        self.period = period / (2*math.pi)

    def gen(self):
        return abs(math.sin(self.t/self.period)*self.mod+self.shift)
