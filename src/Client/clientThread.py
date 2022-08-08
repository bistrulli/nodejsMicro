import requests as req
import numpy as np
import time
from threading import Thread
from pymongo import MongoClient
import pymongo



class clientThread(Thread):
    
    i=0
    toStop=False
    id=None
    mongoClient=None
    
    ttime=None
    delays=[]
    
    def __init__(self,ttime):
        Thread.__init__(self)
        self.ttime=ttime
        self.id=clientThread.i
        clientThread.i+=1
        self.mongoClient=MongoClient("mongodb://localhost:27017/")
        
    
    def run(self):
        ms1Obj=self.mongoClient["sys"]["ms"].find_one({"name":"ms1"})
        while(not clientThread.toStop):
            st = time.time_ns() // 1_000_000 
            
            d = np.random.exponential(scale=self.ttime)
            #clientThread.delays.append(d)
            
            #print(np.mean(clientThread.delayxs))
            
            #lo metto deterministico perche per via dell'imprecisione di timer 
            #i dati non verrebbero puliti
            time.sleep(d/1000.0)
            #pygame.time.delay(int(np.ceil(d)))
            #self.waitEvent.wait(timeout=d/10000.0);
            
            
            reqTime=time.time_ns() // 1_000_000
            req.get('http://localhost:%d/'%(ms1Obj["prxPort"]))
            end= time.time_ns() // 1_000_000
            self.mongoClient["client"]["rt"].insert_one({"st":st,"end":end})
    
    