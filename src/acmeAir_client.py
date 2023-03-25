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

def waitExp(redisCon):
    toStop=redisCon.get("toStop")
    while(toStop!="1"):
        toStop=redisCon.get("toStop")
        time.sleep(2)

def setStart(redisCon):
    redisCon.set("toStop","0")
    
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
                          "hw":1
                          },
                #customeService
                "MSvalidateid":{  "type":"spring",
                          "appFile":"../../acmeair-customerservice-springboot/target/acmeair-customerservice-springboot-2.1.1-SNAPSHOT.jar",
                          "addr":"localhost",
                          "replica":1,
                          "prxFile":prxPath,
                          "hw":45.8597
                          },
                "MSviewprofile":{  "type":"spring",
                          "appFile":"../../acmeair-customerservice-springboot/target/acmeair-customerservice-springboot-2.1.1-SNAPSHOT.jar",
                          "addr":"localhost",
                          "replica":1,
                          "prxFile":prxPath,
                          "hw":1
                          },
                "MSupdateprofile":{"type":"spring",
                          "appFile":"../../acmeair-customerservice-springboot/target/acmeair-customerservice-springboot-2.1.1-SNAPSHOT.jar",
                          "addr":"localhost",
                          "replica":1,
                          "prxFile":prxPath,
                          "hw": 1
                          },
                "MSupdateMiles":{"type":"spring",
                          "appFile":"../../acmeair-customerservice-springboot/target/acmeair-customerservice-springboot-2.1.1-SNAPSHOT.jar",
                          "addr":"localhost",
                          "replica":1,
                          "prxFile":prxPath,
                          "hw":1
                          },
                #booking service
                "MSbookflights":{  "type":"spring",
                          "appFile":"../../acmeair-bookingservice-springboot/target/acmeair-bookingservice-springboot-2.1.1-SNAPSHOT.jar",
                          "addr":"localhost",
                          "replica":1,
                          "prxFile":prxPath,
                          "hw":1
                          },
                "MScancelbooking":{  "type":"spring",
                          "appFile":"../../acmeair-bookingservice-springboot/target/acmeair-bookingservice-springboot-2.1.1-SNAPSHOT.jar",
                          "addr":"localhost",
                          "replica":1,
                          "prxFile":prxPath,
                          "hw":1
                          },
                #flight service
                "MSqueryflights":{  "type":"spring",
                          "appFile":"../../acmeair-flightservice-springboot/target/acmeair-flightservice-springboot-2.1.1-SNAPSHOT.jar",
                          "addr":"localhost",
                          "replica":1,
                          "prxFile":prxPath,
                          "hw":1
                          },
                "MSgetrewardmiles":{  "type":"spring",
                          "appFile":"../../acmeair-flightservice-springboot/target/acmeair-flightservice-springboot-2.1.1-SNAPSHOT.jar",
                          "addr":"localhost",
                          "replica":1,
                          "prxFile":prxPath,
                          "hw":1
                          },
                "acmeair":True
              }
        
        
        redisHost="127.0.0.1"
        msNames=list(msSys.keys());
        pedis=redis.StrictRedis(host=redisHost, port=6379, charset="utf-8", decode_responses=True)
        dry=False
        
        for exp in range(1):
            
            data = {"Cli":[50], "RTm":[], "rtCI":[], "Tm":[], "trCI":[], "ms":[],"NC":[]}
            
            sys = nodeSys(dbHost=redisHost)
            for p in data["Cli"]:
                
                print("####pop %d###" % (p))
                
                pedis.set("users","%d"%(p))
                pedis.publish("users","%d"%(p))  
                
                sys.startClient(p,dry=dry)
                sys.startLoadShape(600,dry=dry,dbHost=redisHost)
                setStart(pedis)
                
                waitExp(pedis)
                    
                print("killing clients")
                sys.stopClient()
    
    except Exception as ex:
        print("Error")
        print("killing clients")
        sys.stopClient()
        print("killing system") 

        
        traceback.print_exception(type(ex), ex, ex.__traceback__)
        
