from threading import Thread
import time
import redis
import numpy as np
#from pymongo import MongoClient
from scipy.io import savemat


class loadShape(Thread):
    
    t=None
    maxt=None
    sys=None
    mntData=None
    keys=["MSauth_hw","MSvalidateid_hw","MSbookflights_hw",
          "MSupdateMiles_hw","MScancelbooking_hw","MSgetrewardmiles_hw",
          "MSqueryflights_hw","MSviewprofile_hw","MSupdateprofile_hw"]
    
    def __init__(self,maxt,sys,dry=False,dbHost="127.0.0.1"):
        Thread.__init__(self)
        self.t=0
        self.sys=sys
        self.maxt=maxt
        self.mntData=[];
        self.dry=dry
        #self.r=redis.Redis(host='localhost', port=6379)
        self.r=redis.StrictRedis(host=dbHost, port=6379, charset="utf-8", decode_responses=True)
        #self.mongoClient = MongoClient(host="mongodb://127.0.0.1:27017/")
    
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
        self.mntShares()
        return self.gen();
    
    def stopSim(self):
        print("stopping simulation")
        # Updating fan quantity form 10 to 25.
        #filter = {'started': 1 }
        # Values to be updated.
        #newvalues = {"$set":{"toStop":1}}
        #self.mongoClient["sys"]["sim"].update_one(filter, newvalues)
        #self.saveMntData()
        self.r.set("toStop","1")
        print("stopped simulation")
    
    def run(self):
        while(self.t<self.maxt):
            self.updateUser(self.tick())
            time.sleep(1)
        self.stopSim()
    
    def mntShares(self):
        ctrl_t=time.time()
        hws=self.r.mget(self.keys)
        u=self.r.get("users")
        self.mntData+=[[str(ctrl_t),u]+hws];
    
    def saveMntData(self):
        print(np.array(self.mntData,dtype=np.str_))
        np.savetxt('ctrldata.csv', np.array(self.mntData,dtype=np.str_), delimiter=",",fmt="%s")
            
    def gen(self):
        pass
    
    def addUsers(self,u):
        pass
    
    def stopUsers(self,u):
        pass