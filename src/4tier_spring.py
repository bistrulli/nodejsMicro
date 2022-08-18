'''
Created on 2 lug 2022

@author: emilio
'''

import time
import traceback

from scipy.io import savemat

from App import nodeSys
import numpy as np
import os


if __name__ == '__main__':
    try:
        data = {"Cli":np.linspace(1,140,35,dtype=int), "RTm":[], "rtCI":[], "Tm":[], "trCI":[], "ms":[],"NC":[]}
        
        msSys = {"ms1":{  "type":"spring",
                          "appFile":"../4tier_spring/ms1/target/4tier-ms1-0.0.1.jar",
                          "addr":"localhost",
                          "replica":1,
                          "prxFile":"../prx/proxy.jar",
                          "hw":15.0253
                          },
                "ms2":{  "type":"spring",
                          "appFile":"../4tier_spring/ms2/target/4tier-ms2-0.0.1.jar",
                          "addr":"localhost",
                          "replica":1,
                          "prxFile":"../prx/proxy.jar",
                          "hw":5.1019 
                          },
                "ms3":{  "type":"spring",
                          "appFile":"../4tier_spring/ms3/target/4tier-ms3-0.0.1.jar",
                          "addr":"localhost",
                          "replica":1,
                          "prxFile":"../prx/proxy.jar",
                          "hw":10.1191
                          }
              }
        
        
        sys = nodeSys()
        for p in data["Cli"]:
            
            print("####pop %d###" % (p))
            
            sys.startSys(msSys=msSys)
            time.sleep(5)
            sys.startClient(p)
            sys.startMNT()
            
            data["ms"] = list(sys.data.keys())
            data["RTm"].append([])
            data["Tm"].append([])
            data["rtCI"].append([])
            data["trCI"].append([])
            data["NC"].append([])
            
            for ms in  data["ms"]:
                data["RTm"][-1].append(sys.data[ms]["rt"][0])
                data["Tm"][-1].append(sys.data[ms]["tr"][0])
                
                data["rtCI"][-1].append(sys.data[ms]["rt"][1])
                data["trCI"][-1].append(sys.data[ms]["tr"][1])
                
                if(ms=="client"):
                    data["NC"][-1].append(1000)
                else:
                    data["NC"][-1].append(msSys[ms]["hw"])
                
            print("####pop %d converged###" % (p))
            savemat("../data/%s_wi5.mat"%(os.path.basename(__file__)), data)
            
            print("killing clients")
            sys.stopClient()
            print("killing system") 
            sys.stopSys()
            sys.reset()
    
    except Exception as ex:
        print("Error")
        print("killing clients")
        sys.stopClient()
        print("killing system") 
        sys.stopSys()
        
        traceback.print_exception(type(ex), ex, ex.__traceback__)
        
