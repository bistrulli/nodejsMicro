from Client import loadShape


class loadShapeAcme_step(loadShape):
    
    def __init__(self,maxt,sys):
        super().__init__(maxt,sys)
        
    def gen(self):
        if((self.t) % 30==0):
            return self.sys.userCount+20
        else:
            return self.sys.userCount
    
    def addUsers(self,nusers):
        self.sys.addUsers(nusers)
    
    def stopUsers(self,users):
        self.sys.stopUsers(users)