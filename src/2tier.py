'''
Created on 2 lug 2022

@author: emilio
'''

from App import nodeSys
import traceback
from scipy.io import savemat
import numpy as np

if __name__ == '__main__':
    try:
        
        data={"pop":[7],"rt":[],"rtCI":[],"tr":[],"trCI":[],"ms":[]}
        
        msSys={"ms1":{"appFile":"../2tier/ms1.js",
                          "addr":"localhost",
                          "port":8081,
                          "mntPort":8082}}
        sys=nodeSys(msSys)
        
        for p in data["pop"]:
            
            print("####pop %d###"%(p))
            
            sys.startSys()
            sys.startClient(p)
            sys.startMNT()
            
            data["ms"]=list(sys.data.keys())
            data["rt"].append([])
            data["tr"].append([])
            data["rtCI"].append([])
            data["trCI"].append([])
            
            for ms in  data["ms"]:
                data["rt"][-1].append(sys.data[ms]["rt"][0])
                data["tr"][-1].append(sys.data[ms]["tr"][0])
                
                data["rtCI"][-1].append(sys.data[ms]["rt"][1])
                data["trCI"][-1].append(sys.data[ms]["tr"][1])
                
            print("####pop %d converged###"%(p))
            savemat("../data/2tier.mat", data)
            
            print("killing clients")
            sys.stopClient()
            print("killing system") 
            sys.stopSys()
            sys.reset()
        
        
    
    except Exception as ex:
        print("killing clients")
        sys.stopClient()
        print("killing system") 
        sys.stopSys()
        
        traceback.print_exception(type(ex), ex, ex.__traceback__)
        
