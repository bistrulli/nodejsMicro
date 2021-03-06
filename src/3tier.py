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
        data = {"Cli":np.linspace(1,50,30,dtype=int), "RTm":[], "rtCI":[], "Tm":[], "trCI":[], "ms":[]}

               # "ms3":{   "appFile":"../3tier/ms3.js",
               #            "addr":"localhost",
               #            "port":8085,
               #            "mntPort":8086},
        msSys = {"ms1":{  "appFile":"../3tier/ms1.js",
                          "addr":"localhost",
                          "port":9081,
                          "prxFile":"../prx/proxy.jar",
                          "prxPort":8081
                          },
                "ms2":{   "appFile":"../3tier/ms2.js",
                          "addr":"localhost",
                          "port":9082,
                          "prxFile":"../prx/proxy.jar",
                          "prxPort":8082}
              }
        sys = nodeSys(msSys)
        
        for p in data["Cli"]:
            
            print("####pop %d###" % (p))
            
            sys.startSys()
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
            savemat("../data/3tier_test_java_jitless.mat", data)
            
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
        
