from threading import Thread, Lock
import time
import redis
import numpy as np

from Client import clientThread
from pymongo import MongoClient


class loadShape(Thread):
    
    t=None
    maxt=None
    
    def __init__(self,maxt):
        Thread.__init__(self)
        self.t=0
        self.maxt=maxt
        self.mongoClient = MongoClient("mongodb://localhost:27017/")
        self.r=redis.Redis(host='localhost', port=6379)
    
    def updateUser(self,users):
        users=int(np.round(users))
        
        if(clientThread.toStop>0):
            raise ValueError("trying to update users when old changes are still doing")
        
        self.r.publish("users", "%d"%(users))
        if(clientThread.userCount<users):
            self.addUsers(users-clientThread.userCount)
        else:
            clientThread.toStop=clientThread.userCount-users;
        
    def tick(self):
        print("tick %d"%(self.t))
        self.t+=1
        return self.gen(self.t);
    
    def stopSim(self):
        print("stopping simulation")
        # Updating fan quantity form 10 to 25.
        filter = {'started': 1 }
        # Values to be updated.
        newvalues = {"$set":{"toStop":1}}
        self.mongoClient["sys"]["sim"].update_one(filter, newvalues)
        print("stopped simulation")
    
    def run(self):
        while(self.t<self.maxt):
            self.updateUser(self.tick())
            time.sleep(1)
        self.stopSim()
            
    def gen(self,t):
        pass
    
    def addUsers(self,u):
        pass