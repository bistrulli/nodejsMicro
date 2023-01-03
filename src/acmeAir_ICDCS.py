'''
Created on 2 lug 2022

@author: emilio
'''

import time
import traceback
import datetime
import redis

from scipy.io import savemat

from App import nodeSys
import numpy as np
import os

from pymongo import MongoClient
import pymongo
import subprocess


def extractKPI(msname):
    subprocess.check_call(["mongoexport","-d",msname,"-c","rt","-f","st,end","--type=csv","-o","../data/ICDCS/%s.csv"%(msname)]);
    
def waitExp():
    mongoClient=MongoClient("mongodb://localhost:27017/")
    
    print("experiment running")
    sim=mongoClient["sys"]["sim"].find_one({})
    while(sim["toStop"]==0):
        time.sleep(1)
        sim=mongoClient["sys"]["sim"].find_one({})
    mongoClient.close()
    
def setStart():
    mongoClient=MongoClient("mongodb://localhost:27017/")
    collist = mongoClient["sys"].list_collection_names()
    # if "sim" in collist:
    #     mongoClient["sys"]["sim"].drop()
    mongoClient["sys"]["sim"].insert_one({"started":1,"toStop":0})
    mongoClient.close()
    
def resetSim():
    mongoClient=MongoClient("mongodb://localhost:27017/")
    collist = mongoClient["sys"].list_collection_names()
    if "sim" in collist:
        mongoClient["sys"]["sim"].drop()
    mongoClient.close()

    


if __name__ == '__main__':
    prxPath="../../msProxy/target/msproxy-0.0.1-SNAPSHOT-jar-with-dependencies.jar"
    try:
        msSys = {#auth service
                "MSauth":{ "type":"spring",
                          "appFile":"../../acmeair-authservice-springboot/target/acmeair-authservice-springboot-2.1.1-SNAPSHOT.jar",
                          "addr":"localhost",
                          "replica":1,
                          "prxFile":prxPath,
                          "hw":10
                          },
                #customeService
                "MSvalidateid":{  "type":"spring",
                          "appFile":"../../acmeair-customerservice-springboot/target/acmeair-customerservice-springboot-2.1.1-SNAPSHOT.jar",
                          "addr":"localhost",
                          "replica":1,
                          "prxFile":prxPath,
                          "hw":10
                          },
                "MSviewprofile":{  "type":"spring",
                          "appFile":"../../acmeair-customerservice-springboot/target/acmeair-customerservice-springboot-2.1.1-SNAPSHOT.jar",
                          "addr":"localhost",
                          "replica":1,
                          "prxFile":prxPath,
                          "hw":10
                          },
                "MSupdateprofile":{"type":"spring",
                          "appFile":"../../acmeair-customerservice-springboot/target/acmeair-customerservice-springboot-2.1.1-SNAPSHOT.jar",
                          "addr":"localhost",
                          "replica":1,
                          "prxFile":prxPath,
                          "hw":10
                          },
                "MSupdateMiles":{"type":"spring",
                          "appFile":"../../acmeair-customerservice-springboot/target/acmeair-customerservice-springboot-2.1.1-SNAPSHOT.jar",
                          "addr":"localhost",
                          "replica":1,
                          "prxFile":prxPath,
                          "hw":10
                          },
                #booking service
                "MSbookflights":{  "type":"spring",
                          "appFile":"../../acmeair-bookingservice-springboot/target/acmeair-bookingservice-springboot-2.1.1-SNAPSHOT.jar",
                          "addr":"localhost",
                          "replica":1,
                          "prxFile":prxPath,
                          "hw":10
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
                          "prxFile":prxPath,
                          "hw":10
                          },
                #flight service
                "MSqueryflights":{  "type":"spring",
                          "appFile":"../../acmeair-flightservice-springboot/target/acmeair-flightservice-springboot-2.1.1-SNAPSHOT.jar",
                          "addr":"localhost",
                          "replica":1,
                          "prxFile":prxPath,
                          "hw":10
                          },
                "MSgetrewardmiles":{  "type":"spring",
                          "appFile":"../../acmeair-flightservice-springboot/target/acmeair-flightservice-springboot-2.1.1-SNAPSHOT.jar",
                          "addr":"localhost",
                          "replica":1,
                          "prxFile":prxPath,
                          "hw":10
                          },
                "acmeair":True
              }
        
        
        msNames=list(msSys.keys());
        pedis=redis.Redis(host='localhost', port=6379)
        
        for exp in range(1):
            
            # if(exp>1):
            #     msSys[msNames[exp-2]]["hw"]=15.0
            # msSys[msNames[exp-1]]["hw"]=4.0
            
            # NCrnd=np.random.rand(10)*9;
            # print(NCrnd)
            # ncIdx=0;
            # for msn in msNames:
            #     if(msn=="acmeair"):
            #         continue
            #     msSys[msn]["hw"]=(NCrnd[ncIdx]+10)
            #     ncIdx+=1
                
            #data = {"Cli":np.linspace(20,220,25,dtype=int), "RTm":[], "rtCI":[], "Tm":[], "trCI":[], "ms":[],"NC":[]}
            data = {"Cli":[30.0], "RTm":[], "rtCI":[], "Tm":[], "trCI":[], "ms":[],"NC":[]}
            
            sys = nodeSys()
            for p in data["Cli"]:
                
                print("####pop %d###" % (p))
                
                sys.startSys(msSys=msSys)
                time.sleep(5)
                
                pedis.set("users","%d"%(p))
                pedis.publish("users","%d"%(p))  
                
                sys.startClient(p)
                #sys.startLoadShape(180)
                setStart()
                #waitExp()
                time.sleep(180)
                
                data["ms"] = list(msSys.keys())
                data["RTm"].append([])
                data["Tm"].append([])
                data["rtCI"].append([])
                data["trCI"].append([])
                data["NC"].append([])
                
                for ms in  data["ms"]:
                    if(ms=="acmeair"):
                        continue
                    
                    print("saving",ms)
                    extractKPI(ms)
                    # if(ms=="client"):
                    #     data["NC"][-1].append(1000)
                    # else:
                    #     data["NC"][-1].append(msSys[ms]["hw"])
                
                extractKPI("client")
                
                print("####pop %d converged###" % (p))
                #savemat("../data/ICDCS/%s_full_%d_m1.mat"%(os.path.basename(__file__),exp+1), data)
                
                print("killing clients")
                sys.stopClient()
                print("killing system") 
                sys.stopSys()
                sys.reset()
                resetSim()
    
    except Exception as ex:
        print("Error")
        print("killing clients")
        sys.stopClient()
        print("killing system") 
        sys.stopSys()
        resetSim()
        
        traceback.print_exception(type(ex), ex, ex.__traceback__)
        
