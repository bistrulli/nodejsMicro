from Client import loadShape
from Client import clientProcess_acme
from App import nodeSys


class loadShapeAcme_step(loadShape):
    
    def __init__(self,maxt):
        super().__init__(maxt)
        
    def gen(self,t):
        if((self.t) % 30==0):
            return nodeSys.nodeSys.userCount+20
        else:
            return nodeSys.nodeSys.userCount
    
    def addUsers(self,nusers):
        for i in range(nusers):
            u=clientProcess_acme(ttime=200,id=nodeSys.userId)
            u.start()
            nodeSys.nodeSys.userCount+=1
            nodeSys.nodeSys.userId+=1
    
    def stopUsers(self,u):
        for i in range(u):
            nodeSys.clientProc[i].terminate();
            nodeSys.clientProc[i].join()
            nodeSys.nodeSys.userCount-=1;