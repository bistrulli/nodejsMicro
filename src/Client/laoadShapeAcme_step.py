from threading import Thread, Lock

from Client import loadShape
from Client import clientThread_acme
from Client import clientThread


class loadShapeAcme_step(loadShape):
    
    def __init__(self,maxt):
        super().__init__(maxt)
        
    def gen(self,t):
        if((self.t) % 1000==0):
            return clientThread.userCount+20
        else:
            return clientThread.userCount
    
    def addUsers(self,nusers):
        for i in range(nusers):
            u=clientThread_acme(ttime=200)
            u.start()