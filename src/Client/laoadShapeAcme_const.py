from Client import loadShape


class loadShapeAcme_const(loadShape):
    
    def __init__(self,maxt,sys,dry=False,dbHost="127.0.0.1",datadir=None):
        super().__init__(maxt,sys,dry,dbHost,datadir)
        
    def gen(self):
        return self.sys.userCount