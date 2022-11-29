import time
import numpy as np

from pymongo import MongoClient
import multiprocessing


class clientProcess(multiprocessing.Process):
    
    toStop = False
    id = None
    mongoClient = None
    ttime = None
    
    def __init__(self, ttime,id):
        super().__init__()
        self.ttime = ttime
        self.id = id
        
    def think(self):
        d = np.random.exponential(scale=self.ttime)
        time.sleep(d/1000.0)
        
    def stop(self):
        self.toStop=True
    
    def run(self):
        self.mongoClient = MongoClient(host="mongodb://127.0.0.1:27017/")
        while(True):
            st = time.time_ns() // 1_000_000 
            self.think()
            self.userLogic()
            end = time.time_ns() // 1_000_000
            self.mongoClient["client"]["rt"].insert_one({"st":st, "end":end})
        
    def userLogic(self):
        print("should subclass")
    
    # def isToKill(self):
    #     toKill=False;
    #     clientThread.l1.acquire()
    #     if(clientThread.toStop is not None and clientThread.toStop>0):
    #         clientThread.toStop-=1
    #         toKill=True
    #     clientThread.l1.release()
    #     return toKill
    #
    # def decreaseUser(self):
    #     clientThread.l2.acquire()
    #     clientThread.userCount-=1
    #     clientThread.l2.release()
    #
    # def increaseUser(self):
    #     print("added user %d"%(self.id))
    #     clientThread.l2.acquire()
    #     clientThread.usersThreads.append(self)
    #     clientThread.userCount+=1
    #     clientThread.l2.release()

if __name__ == '__main__':
    p=clientProcess(500.0,1)
    p.start()
    time.sleep(10)
    p.terminate()
    p.join()
    print("exit")
    