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
    
    def __init__(self,ttime):
        Thread.__init__(self)
        self.ttime=ttime
        self.id=clientThread.i
        clientThread.i+=1
        self.mongoClient=MongoClient("mongodb://localhost:27017/client")
    
    def run(self):
        while(not clientThread.toStop):
            st = time.time_ns() // 1_000_000 
            
            delay = np.random.exponential(scale=self.ttime)
            time.sleep(delay)
            
            reqTime=time.time_ns() // 1_000_000
            req.get('http://localhost:8081/%d'%(reqTime))
            
            end= time.time_ns() // 1_000_000
            
            self.mongoClient["client"]["rt"].insert_one({"st":st,"end":end})
    
    