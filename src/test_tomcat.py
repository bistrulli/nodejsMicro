'''
Created on 6 ago 2022

@author: emilio
'''
import requests as req
import numpy as np
import time
from threading import Thread, Lock




class testThread(Thread):
    
    i=0
    toStop=False
    id=None
    nrq=0
    lock = Lock()
    mongoClient=None
    
    ttime=None
    delays=[]
    
    def __init__(self,ttime):
        Thread.__init__(self)
        self.ttime=ttime
        self.id=testThread.i        
    
    def run(self):
        while(not testThread.toStop):
            #st = time.time_ns() // 1_000_000 
            
            #d = np.random.exponential(scale=self.ttime)
            
            time.sleep(self.ttime/1000.0)
            
            reqTime=time.time_ns() // 1_000_000
            
            req.get('http://localhost:80/greeting')
            #end= time.time_ns() // 1_000_000
            
            testThread.lock.acquire()
            testThread.nrq+=1
            testThread.lock.release()
            

if __name__ == '__main__':
    
    ttime=10.0
    nusers=30
    users=[testThread(ttime) for i in range(nusers)]
    
    st=time.time_ns()
    for u in users:
        u.start()
    
    for i in range(100):
        time.sleep(1)
        print(testThread.nrq*10**9/(time.time_ns()-st),i)
    
    testThread.toStop=True
    for u in users:
        u.join()
        print(u.id," killed")
    