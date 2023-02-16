from Client import loadShape


class StepShape(loadShape):
    def __init__(self, maxt,sys,dry=False,dbHost="127.0.0.1",datadir=None,intervals, values):
        super().__init__(maxt,sys,dry,dbHost,datadir)
        
        assert len(intervals) == len(values)
        self.intervals = intervals
        self.values = values

    def gen(self):
        i = 0
        while i < len(self.intervals) and self.t >= self.intervals[i]:
            i += 1
        return self.values[min(i, len(self.values)-1)]
