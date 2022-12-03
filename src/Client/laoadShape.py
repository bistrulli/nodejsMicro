from threading import Thread
import time
import redis
import numpy as np
from App import nodeSys


class loadShape(Thread):
    
    t=None
    maxt=None
    sys=None
    
    def __init__(self,maxt,sys):
        Thread.__init__(self)
        self.t=0
        self.sys=sys
        self.maxt=maxt
        self.r=redis.Redis(host='localhost', port=6379)
    
    def updateUser(self,users):
        users=int(np.round(users))
        
        self.r.set("users","%d"%(users))
        self.r.publish("users", "%d"%(users))
        if(self.sys.userCount<users):
            self.addUsers(users-self.sys.userCount)
        else:
            self.stopUsers(self.sys.userCount-users)
            
       
        
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
    
    def stopUsers(self,u):
        pass