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
        data = {"Cli":np.linspace(1,140,30,dtype=int), "RTm":[], "rtCI":[], "Tm":[], "trCI":[], "ms":[]}

        msSys = {"ms2":{  "type":"spring",
                          "appFile":"../3tier_spring/3tier_ms2/target/3tier-ms2-0.0.1.jar",
                          "addr":"localhost",
                          "replica":1,
                          "prxFile":"../prx/proxy.jar",
                          "hw":4.0
                          },
                "ms1":{  "type":"spring",
                          "appFile":"../3tier_spring/3tier_ms1/target/3tier-ms1-0.0.1.jar",
                          "addr":"localhost",
                          "replica":1,
                          "prxFile":"../prx/proxy.jar",
                          "hw":20.0
                          }
              }
        
        
        sys = nodeSys()
        
        for p in data["Cli"][8:]:
            
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
            
            for ms in  data["ms"]:
                data["RTm"][-1].append(sys.data[ms]["rt"][0])
                data["Tm"][-1].append(sys.data[ms]["tr"][0])
                
                data["rtCI"][-1].append(sys.data[ms]["rt"][1])
                data["trCI"][-1].append(sys.data[ms]["tr"][1])
                
            print("####pop %d converged###" % (p))
            savemat("../data/%s_3.mat"%(os.path.basename(__file__)), data)
            
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
        print("clear saved log")
        sys.clearLog()
        
        traceback.print_exception(type(ex), ex, ex.__traceback__)
        
