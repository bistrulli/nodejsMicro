from threading import Thread, Lock
import time
import numpy as np

from pymongo import MongoClient


class clientThread(Thread):
    
    i = 0
    userCount = 0
    toStop = False
    id = None
    mongoClient = None
    toStop = 0
    l1=Lock()
    l2=Lock()
    usersThreads = []
    ttime = None
    
    def __init__(self, ttime):
        Thread.__init__(self)
        self.ttime = ttime
        self.id = clientThread.i
        clientThread.i += 1
        self.increaseUser()
        self.mongoClient = MongoClient(host="mongodb://127.0.0.1:27017/")
    
    def think(self):
        d = np.random.exponential(scale=self.ttime)
        time.sleep(d/1000.0)
    
    def run(self):
        while(True):
            st = time.time_ns() // 1_000_000 
            self.think()
            self.userLogic()
            end = time.time_ns() // 1_000_000
            self.mongoClient["client"]["rt"].insert_one({"st":st, "end":end})
            if(self.isToKill()):
                break;
        self.decreaseUser();
        
    def userLogic(self):
        pass
    
    def isToKill(self):
        toKill=False;
        clientThread.l1.acquire()
        if(clientThread.toStop is not None and clientThread.toStop>0):
            clientThread.toStop-=1
            toKill=True
        clientThread.l1.release()
        return toKill
    
    def decreaseUser(self):
        clientThread.l2.acquire()
        clientThread.userCount-=1
        clientThread.l2.release()
        
    def increaseUser(self):
        print("added user %d"%(self.id))
        clientThread.l2.acquire()
        clientThread.usersThreads.append(self)
        clientThread.userCount+=1
        clientThread.l2.release()