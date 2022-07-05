from Monitoring import mnt_thread
from Client import clientThread
import  time


class mnt_thread_local(mnt_thread):
    
    lastrtSample=None
    
    def __init__(self,ms,period,name,stime):
        super().__init__(ms,period,name,stime)
        self.lastrtSample=0
    
    def getMSData(self):
        res={"nrq":clientThread.nrq,"rt":clientThread.rt[self.lastrtSample:]}
        self.lastrtSample+=len(res["rt"])
        res["nrq"]=self.getTRData()
        
        return res
    
    def getTRData(self):
        # EVTdata = clientThread.evt 
        
        tsim=time.time_ns() // 1_000_000
        if(not self.lnrrq or self.lnrrq is None):
            Ti=(clientThread.nrq*1000.0)/(tsim-self.stime)
            self.lnrrq=(Ti*(tsim-self.stime)/(1000.0))
        else:
            Ti=((clientThread.nrq-self.lnrrq)*1000)/(tsim-self.lsample)
            self.lnrrq=(Ti*(tsim-self.lsample)/(1000.0))+self.lnrrq
    
        self.lsample=tsim
        
        # k=0
        # bi=0
        # K=[]
        # if(len(EVTdata)>0):
        #     t0=EVTdata[0]["st"]*1.0
             
            #print("#######%f######"%((clientThread.nrq*1000)/(tsim-self.stime)))
            # for i in range(len(EVTdata)):
            #     #EVTdata[i]["st"]-=t0
            #     #EVTdata[i]["end"]-=t0
            #     if(EVTdata[i]["end"]<=((k+1)*1000+self.stime) and (EVTdata[i]["end"])>=(k*1000)+self.stime):
            #         bi+=1
            #     else:
            #         K.append(bi)
            #         k+=1
            #         bi=0
            
        return Ti;
            
        