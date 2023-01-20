import time
import numpy as np

#from pymongo import MongoClient
import multiprocessing


class clientProcess(multiprocessing.Process):
    
    toStop = False
    id = None
    mongoClient = None
    ttime = None
    dbHost="185.10.17.121"
    remoteHost="185.10.17.121"
    
    def __init__(self, ttime,cId,dry=False):
        super().__init__()
        self.ttime = ttime
        self.id = cId
        self.dry = dry
        print("started process id=%d"%(self.id))
        
    def think(self):
        d = np.random.exponential(scale=self.ttime)
        time.sleep(d/1000.0)
        
    def stop(self):
        self.toStop=True
    
    def run(self):
        #self.mongoClient = MongoClient(host="mongodb://%s:27017/"%(clientProcess.dbHost))
        while(True):
            st = time.time_ns() // 1_000_000 
            self.think()
            if(not self.dry):
                self.userLogic()
            end = time.time_ns() // 1_000_000
            #self.mongoClient["client"]["rt"].insert_one({"st":st, "end":end})
        
    def userLogic(self):
        print("should subclass")
    