from Client import loadShape


class loadShapeAcme_step(loadShape):
    
    def __init__(self,maxt,sys,dry=False,dbHost="127.0.0.1"):
        super().__init__(maxt,sys,dry,dbHost)
        
    def gen(self):
        if(self.t % 30==0 and self.t<=600):
            return self.sys.userCount+10
        elif(self.t % 30==0 and self.t>=700):
            return max(self.sys.userCount-10,10)
        else:
            return self.sys.userCount
    
    def addUsers(self,nusers):
        self.sys.addUsers(nusers,self.dry)
    
    def stopUsers(self,users):
        self.sys.stopUsers(users)