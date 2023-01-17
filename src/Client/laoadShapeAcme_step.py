from Client import loadShape


class loadShapeAcme_step(loadShape):
    
    def __init__(self,maxt,sys,dry=False):
        super().__init__(maxt,sys,dry)
        
    def gen(self):
        if(self.t % 30==0 and self.t<=-1):
            return self.sys.userCount+30
        else:
            return self.sys.userCount
    
    def addUsers(self,nusers):
        self.sys.addUsers(nusers,self.dry)
    
    def stopUsers(self,users):
        self.sys.stopUsers(users)