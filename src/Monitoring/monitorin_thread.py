import requests as req
import numpy as np
import time
from threading import Thread
from BatchMeans import BM
import json
from pymongo import MongoClient
import pymongo

class mnt_thread(Thread):
    
    ms=None
    rtData=None
    trData=None
    period=None
    toStop=False
    name=None
    
    rtBm=None
    trBm=None
    
    trRowData=None
    stime=None
    
    lnrrq=None
    mongoClient=None
    msDb=None
    
    
    def __init__(self,ms,period,name,stime=None):
        Thread.__init__(self)
        self.ms=ms
        self.period=period
        self.rtData=None
        self.trData=None
        self.toStop=False
        self.name=name
        self.trRowData=[]
        self.stime=stime
        self.lnrrq=None
        self.mongoClient=MongoClient("mongodb://localhost:27017/"+self.name)
        self.lastEvent=-1
        
        self.rtBm=BM(B=30,K=30,P=.95,wupH=100,name="rt-"+self.name)
        self.trBm=BM(B=30,K=30,P=.95,wupH=100,name="tr-"+self.name)
    
    def getTRData(self):
        res = req.get("http://%s:%d/Events/"%(self.ms["addr"],self.ms["mntPort"]))
        EVTdata = json.loads(res.text)
        
        k=0
        bi=0
        K=[]
        if(len(EVTdata["evt"])>0):
            t0=EVTdata["evt"][0]["st"]
            
            for i in range(len(EVTdata["evt"])):
                EVTdata["evt"][i]["st"]-=t0
                EVTdata["evt"][i]["end"]-=t0
                if(EVTdata["evt"][i]["end"]<= (k+1)*1000 and EVTdata["evt"][i]["end"]>=k*1000):
                    bi+=1
                else:
                    K.append(bi)
                    k+=1
                    bi=0
        
        return K;
        

    #funzione che contatta iil microservizio e torna i dati misurati
    def getMSData(self):
        res={"rt":None,"nrq":None}
        
        rtData=[]
        cursor=None
        
        tsim=time.time_ns() // 1_000_000
        if(self.lnrrq is None):
            cursor=self.mongoClient[self.name]["rt"].find().sort("st",1)
        else:
            cursor=self.mongoClient[self.name]["rt"].find({ "st": { "$gt": self.lastEvent } }).sort("st",1)
        nrq=self.mongoClient[self.name]["rt"].count_documents({})
            
        for item in cursor:
            rtData.append(int(item["end"])-int(item["st"]))
            self.lastEvent=item["st"]
            
            #print(int(item["end"]),int(item["st"]))
        
        #print(rtData)
            
        if(self.lnrrq is None):
            Ti=(nrq*1000)/(tsim-self.stime)
        else:
            Ti=((nrq-self.lnrrq)*1000)/(tsim-self.lsample)
        
        
        self.lnrrq=nrq
        self.lsample=tsim
        
        res["rt"]=rtData
        res["nrq"]=Ti
           
        return res
    
    def getData(self):
        return [self.rtData,self.trData]
    
    def run(self):
        
        rtConveerged=False
        trConveerged=False
        stl=None
        while(not rtConveerged or not trConveerged):
            if(stl is not None):
                delay=max(self.period-(time.time()-stl),0)
            else:
                delay=self.period
            
            
            time.sleep(delay)
            
            stl=time.time()                
            data=self.getMSData()
            
            #devo aggiungere il throughput
            self.rtBm.samples.extend(data["rt"])
            rtRes=self.rtBm.BM()
            
            self.trBm.samples.append(data["nrq"])
            trRes=self.trBm.BM()
            
            ert=None
            if(rtRes is not None):
                ert=rtRes[1]*100/rtRes[0]
                self.rtData=rtRes
                if(ert<=0.5):
                    rtConveerged=True
                    print("rt-%s converged <%.4f +/- %.4f>"%(self.name,rtRes[0],rtRes[1]))
                else:
                    print("rt-%s converging <%.4f +/- %.4f>"%(self.name,rtRes[0],rtRes[1]))
            
            etr=None
            if(trRes is not None):
                etr=trRes[1]*100/trRes[0]
                self.trData=trRes
                if(etr<=0.5):
                    trConveerged=True
                    print("tr-%s converged <%.4f +/- %.4f>"%(self.name,trRes[0],trRes[1]))
                else:
                    print("tr-%s converging <%.4f +/- %.4f>"%(self.name,trRes[0],trRes[1]))
            
            
            
        