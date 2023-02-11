from Client import loadShape
from scipy.io import loadmat
import os

class loadShapeAcme_twt(loadShape):
    
    def __init__(self,maxt,sys,dry=False,dbHost="127.0.0.1",datadir=None):
        super().__init__(maxt,sys,dry,dbHost,datadir)
        
        absolute_path = os.path.dirname(__file__)
        trace_path = os.path.join(absolute_path, "twitter_20210101_730-24_freq120sec.mat")
        self.tweetTrace=loadmat(trace_path)["tweets"][0]
        self.tweetTrace=(self.tweetTrace-min(self.tweetTrace))/(max(self.tweetTrace)-min(self.tweetTrace))*50+15
        
    def gen(self):
        return self.tweetTrace[self.t % self.tweetTrace.shape[0]]