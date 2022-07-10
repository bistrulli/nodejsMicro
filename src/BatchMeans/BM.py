import numpy as np
from scipy import stats

class BM():
    B=None
    K=None
    samples=None
    Batches=None
    P=None
    wupIdx=None
    wupH=None
    name=None
    logfile=None
    
    def __init__(self,B,K,P,wupH,name,logFile):
        self.B=B
        self.K=K
        self.P=P
        self.wupH=wupH
        self.wupIdx=None
        self.samples=[]
        self.Batches=[]
        self.name=name
        self.logfile=logFile
        
    def warmUp(self):
        e=None
        if(len(self.samples)>self.wupH):
            e=np.mean(np.abs(np.diff(self.cumMean()))[len(self.samples)-self.wupH:])
            if(e<10**(0)):
                self.wupIdx=len(self.samples)-1
                self.logfile.write("[%s]warmUP completed with avg error %f:\n"%(self.name,e))
            else:
                self.logfile.write("[%s]warmUP-error %f:\n"%(self.name,e))
        else:
            self.logfile.write("[%s]warn-up %d %d:\n"%(self.name,len(self.samples),self.wupH))
    
    def BM(self):
        res=None
        
        if(self.wupIdx is None):
            self.warmUp()
        else:
            ss_samples=self.samples[self.wupIdx:-1]
            if(len(ss_samples)//self.B>=self.K):
                Kr=(len(ss_samples))//self.B
                
                if(self.Batches is None):
                    self.Batches=[[ss_samples[self.B*k+b] for b in range(self.B)] for k in range(Kr)]
                else:
                    self.Batches.extend([[ss_samples[self.B*k+b] for b in range(self.B)] for k in range(len(self.Batches)-1,Kr)])
                
                Sb2=1.0/(Kr-1)*np.var(np.mean(self.Batches,axis=1))
                Y=np.mean(np.mean(self.Batches,axis=1))
                CI=np.abs(stats.t.ppf((1-self.P)/2, Kr-1)*(np.sqrt(Sb2)/np.sqrt(Kr)))
            
                res=[Y,CI]
            else:
                self.logfile.write("[%s]Accumulating BatchMeans samples %d of %d\n"%(self.name,len(ss_samples),self.B*self.K))
        
        return res

    def cumMean(self):
        return np.divide(np.cumsum(self.samples),np.linspace(1,len(self.samples),len(self.samples)))

if __name__=='__main__':

    h=100
    
    bm=BM(B=30,K=30,P=.95,wupH=100)
    
    while (True):
        ttime=1
        bm.samples.append(np.random.exponential(scale=ttime))
        res=bm.BM()
        if(res is not None):
            e=res[1]*100/res[0]
            if(e<1):
                break
            else:
                print(e)
            
    print(res[0],"+/-",res[1],res[1]*100/res[0])
    print(len(bm.samples))