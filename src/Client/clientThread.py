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
    
    def think(self):
        #d = np.random.exponential(scale=self.ttime)
        time.sleep(self.ttime/1000.0)
        
    
    def run(self):
        pass
    
    