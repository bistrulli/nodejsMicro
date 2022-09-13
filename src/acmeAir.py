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
        data = {"Cli":[1], "RTm":[], "rtCI":[], "Tm":[], "trCI":[], "ms":[],"NC":[]}
        
        msSys = {#auth service
                "MSauth":{ "type":"spring",
                          "appFile":"../../acmeair-authservice-springboot/target/acmeair-authservice-springboot-2.1.1-SNAPSHOT.jar",
                          "addr":"localhost",
                          "replica":1,
                          "prxFile":"../prx/proxy.jar",
                          "hw":15
                          },
                #customeService
                "MSvalidateid":{  "type":"spring",
                          "appFile":"../../acmeair-customerservice-springboot/target/acmeair-customerservice-springboot-2.1.1-SNAPSHOT.jar",
                          "addr":"localhost",
                          "replica":1,
                          "prxFile":"../prx/proxy.jar",
                          "hw":15
                          },
                "MSviewprofile":{  "type":"spring",
                          "appFile":"../../acmeair-customerservice-springboot/target/acmeair-customerservice-springboot-2.1.1-SNAPSHOT.jar",
                          "addr":"localhost",
                          "replica":1,
                          "prxFile":"../prx/proxy.jar",
                          "hw":15
                          },
                "MSupdateprofile":{"type":"spring",
                          "appFile":"../../acmeair-customerservice-springboot/target/acmeair-customerservice-springboot-2.1.1-SNAPSHOT.jar",
                          "addr":"localhost",
                          "replica":1,
                          "prxFile":"../prx/proxy.jar",
                          "hw":15.0
                          },
                "MSupdateMiles":{"type":"spring",
                          "appFile":"../../acmeair-customerservice-springboot/target/acmeair-customerservice-springboot-2.1.1-SNAPSHOT.jar",
                          "addr":"localhost",
                          "replica":1,
                          "prxFile":"../prx/proxy.jar",
                          "hw":15.0
                          },
                #booking service
                "MSbookflights":{  "type":"spring",
                          "appFile":"../../acmeair-bookingservice-springboot/target/acmeair-bookingservice-springboot-2.1.1-SNAPSHOT.jar",
                          "addr":"localhost",
                          "replica":1,
                          "prxFile":"../prx/proxy.jar",
                          "hw":15
                          },
                # "MSbybookingnumber":{  "type":"spring",
                #           "appFile":"../../acmeair-bookingservice-springboot/target/acmeair-bookingservice-springboot-2.1.1-SNAPSHOT.jar",
                #           "addr":"localhost",
                #           "replica":1,
                #           "prxFile":"../prx/proxy.jar",
                #           "hw":15
                #           },
                # "MSbyuser":{  "type":"spring",
                #           "appFile":"../../acmeair-bookingservice-springboot/target/acmeair-bookingservice-springboot-2.1.1-SNAPSHOT.jar",
                #           "addr":"localhost",
                #           "replica":1,
                #           "prxFile":"../prx/proxy.jar",
                #           "hw":15
                #           },
                "MScancelbooking":{  "type":"spring",
                          "appFile":"../../acmeair-bookingservice-springboot/target/acmeair-bookingservice-springboot-2.1.1-SNAPSHOT.jar",
                          "addr":"localhost",
                          "replica":1,
                          "prxFile":"../prx/proxy.jar",
                          "hw":15
                          },
                #flight service
                "MSqueryflights":{  "type":"spring",
                          "appFile":"../../acmeair-flightservice-springboot/target/acmeair-flightservice-springboot-2.1.1-SNAPSHOT.jar",
                          "addr":"localhost",
                          "replica":1,
                          "prxFile":"../prx/proxy.jar",
                          "hw":15
                          },
                "MSgetrewardmiles":{  "type":"spring",
                          "appFile":"../../acmeair-flightservice-springboot/target/acmeair-flightservice-springboot-2.1.1-SNAPSHOT.jar",
                          "addr":"localhost",
                          "replica":1,
                          "prxFile":"../prx/proxy.jar",
                          "hw":15
                          },
                "acmeair":True
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
            savemat("../data/%s_wi.mat"%(os.path.basename(__file__)), data)
            
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
        
