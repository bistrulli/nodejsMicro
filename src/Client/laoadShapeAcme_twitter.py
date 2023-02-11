from Client import loadShape
from scipy.io import loadmat

class loadShapeAcme_twt(loadShape):
    
    def __init__(self,maxt,sys,dry=False,dbHost="127.0.0.1",datadir=None):
        super().__init__(maxt,sys,dry,dbHost,datadir)
        self.tweetTrace=loadmat("twitter_20210101_730-24_freq120sec.mat")["tweets"][0]
        self.tweetTrace=(self.tweetTrace-min(self.tweetTrace))/(max(self.tweetTrace)-min(self.tweetTrace))*50+15
        
    def gen(self):
        return self.tweetTrace[self.t % self.tweetTrace.shape[0]]