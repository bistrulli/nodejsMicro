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
from Client import loadShapeAcme_const
from Client import loadShapeAcme_step


def extractKPI(msname,datadir):
    subprocess.check_call(["mongoexport","-d",msname,"-c","rt","-f","st,end","--type=csv","-o","%s/%s.csv"%(datadir,msname)]);
    
# def waitExp():
#     mongoClient=MongoClient("mongodb://localhost:27017/")
#
#     print("experiment running")
#     sim=mongoClient["sys"]["sim"].find_one({})
#     while(sim["toStop"]==0):
#         time.sleep(1)
#         sim=mongoClient["sys"]["sim"].find_one({})
#     mongoClient.close()

def waitExp(redisCon):
    toStop=redisCon.get("toStop")
    while(toStop!="1"):
        toStop=redisCon.get("toStop")
        time.sleep(2)
    
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
                          "hw":300
                          },
                #customeService
                "MSvalidateid":{  "type":"spring",
                          "appFile":"../../acmeair-customerservice-springboot/target/acmeair-customerservice-springboot-2.1.1-SNAPSHOT.jar",
                          "addr":"localhost",
                          "replica":1,
                          "prxFile":prxPath,
                          "hw":300
                          },
                "MSviewprofile":{  "type":"spring",
                          "appFile":"../../acmeair-customerservice-springboot/target/acmeair-customerservice-springboot-2.1.1-SNAPSHOT.jar",
                          "addr":"localhost",
                          "replica":1,
                          "prxFile":prxPath,
                          "hw":300
                          },
                "MSupdateprofile":{"type":"spring",
                          "appFile":"../../acmeair-customerservice-springboot/target/acmeair-customerservice-springboot-2.1.1-SNAPSHOT.jar",
                          "addr":"localhost",
                          "replica":1,
                          "prxFile":prxPath,
                          "hw": 300
                          },
                "MSupdateMiles":{"type":"spring",
                          "appFile":"../../acmeair-customerservice-springboot/target/acmeair-customerservice-springboot-2.1.1-SNAPSHOT.jar",
                          "addr":"localhost",
                          "replica":1,
                          "prxFile":prxPath,
                          "hw":300
                          },
                #booking service
                "MSbookflights":{  "type":"spring",
                          "appFile":"../../acmeair-bookingservice-springboot/target/acmeair-bookingservice-springboot-2.1.1-SNAPSHOT.jar",
                          "addr":"localhost",
                          "replica":1,
                          "prxFile":prxPath,
                          "hw":300
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
                          "hw":300
                          },
                #flight service
                "MSqueryflights":{  "type":"spring",
                          "appFile":"../../acmeair-flightservice-springboot/target/acmeair-flightservice-springboot-2.1.1-SNAPSHOT.jar",
                          "addr":"localhost",
                          "replica":1,
                          "prxFile":prxPath,
                          "hw":300
                          },
                "MSgetrewardmiles":{  "type":"spring",
                          "appFile":"../../acmeair-flightservice-springboot/target/acmeair-flightservice-springboot-2.1.1-SNAPSHOT.jar",
                          "addr":"localhost",
                          "replica":1,
                          "prxFile":prxPath,
                          "hw":300
                          },
                "acmeair":True
              }
        
        
        msNames=list(msSys.keys());
        redisHost="127.0.0.1"
        pedis=redis.StrictRedis(host=redisHost, port=6379, charset="utf-8", decode_responses=True)
        dry=False
        
        for exp in range(10):
            
            data = {"Cli":[50], "RTm":[], "rtCI":[], "Tm":[], "trCI":[], "ms":[],"NC":[]}
            sys = nodeSys(dbHost=redisHost)
            
            for p in data["Cli"]:
                
                ctrl={"name":"atom_const50","workDir":"/home/virtual/git/atom-replication/GA/",
                      "ctrlCmd":"matlab -nodesktop -nosplash -nodisplay -nojvm -r main(3) quit;"}
                
                # ctrl={"name":"muopt_const50","workDir":"/home/virtual/git/atom-replication/LQN-CRN/controller/acmeAir/",
                #       "ctrlCmd":"julia acmeCtrl.jl"}
                
                datadir="../data/revision2/ctrl/%s_%d/"%(ctrl["name"],exp)
                os.makedirs( datadir, exist_ok=True)
                
                print("####pop %d###" % (p))
                sys.startSys(msSys=msSys)
                time.sleep(5)
                print("sys started")
                
                pedis.set("users","%d"%(p))
                pedis.publish("users","%d"%(p))
                
                sys.startCtrl(ctrl,pedis)
                print("ctrl started")  
                
                #lancio i client iniziali
                sys.startClient(p,dry=dry)
                #lancio la forma del carico e i sistemi di monitoring
                lshape=loadShapeAcme_const(maxt=1200,sys=sys,dry=dry,dbHost=redisHost,datadir=datadir)
                lshape.start()
                #attendo la fine dell'esperiemnto
                setStart()
                waitExp(pedis)
                #time.sleep(380)
                
                data["ms"] = list(msSys.keys())
                data["RTm"].append([])
                data["Tm"].append([])
                data["rtCI"].append([])
                data["trCI"].append([])
                data["NC"].append([])
                
                
                if(not dry):
                    for ms in  data["ms"]:
                        if(ms=="acmeair"):
                            continue
                        
                        print("saving",ms)
                        extractKPI(ms,datadir)
                    extractKPI("client",datadir)
                    
                print("killing clients")
                sys.stopClient()
                print("killing system") 
                sys.stopSys()
                sys.reset()
                resetSim()
                print("killing ctrl")
                sys.ctrlProc.terminate()
                print("killed ctrl");
    
    except Exception as ex:
        print("Error")
        print("killing clients")
        sys.stopClient()
        print("killing system") 
        sys.stopSys()
        resetSim()
        print("killing ctrl")
        sys.ctrlProc.kill()
        
        traceback.print_exception(type(ex), ex, ex.__traceback__)
        
