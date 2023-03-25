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
import argparse
import subprocess

from Client import loadShapeAcme_step
from Client import loadShapeAcme_twt
from Client import SinShape
from Client import StepShape


def getCliOptions():
    parser = argparse.ArgumentParser(description='muOpt Experiments Runner')
    parser.add_argument('ctrl', choices=['muopt', 'atom'],help='specify the controller to use')
    parser.add_argument("load",choices=["step_slow","sin","step",'tweeter_7_8',"wc98"],help='specify the load shape to use')
    args = parser.parse_args()
    return args

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
    
def getCtrl(ctrlName,loadName):
    ctrl=None
    if(ctrlName=="muopt"):
        ctrl={"name":"julia_%s"%(loadName),"workDir":"/home/virtual/git/atom-replication/LQN-CRN/controller/acmeAir/",
          "ctrlCmd":"julia acmeCtrl.jl"}
    elif(ctrlName=="atom"):
        ctrl={"name":"atom_%s"%(loadName),"workDir":"/home/virtual/git/atom-replication/GA/",
         "ctrlCmd":"matlab -nodesktop -nosplash -nodisplay -nojvm -r main(3) quit;"}
        
    return ctrl


def startLoadShape(loadName):
    lshape=None
    if(loadName=="step_slow"):
        lshape=StepShape(maxt=2000,sys=sys,dry=dry,dbHost=redisHost,datadir=datadir,intervals=None, values=None,shapeData="stepshape_slow")
    elif(loadName=="sin"):
        lshape=SinShape(maxt=500,sys=sys,dry=dry,dbHost=redisHost,datadir=datadir, mod=25., shift=35., period=200)
    elif(args.load=="step"):
        lshape=StepShape(maxt=2000,sys=sys,dry=dry,dbHost=redisHost,datadir=datadir,intervals=None, values=None,shapeData="stepshape")
    elif(loadName=="twitter"):
        lshape=loadShapeAcme_twt(maxt=2000,sys=sys,dry=dry,dbHost=redisHost,datadir=datadir)
    elif(loadName=="wc98"):
        lshape=loadShapeAcme_twt(maxt=2000,sys=sys,dry=dry,dbHost=redisHost,datadir=datadir,trace="wc98.mat")
    else:
        raise ValueError("Load not recognized")
    lshape.start()

    

if __name__ == '__main__':
    
    args=getCliOptions()
    
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
        
        #here the host where redis is installed
        redisHost="127.0.0.1"
        msNames=list(msSys.keys());
        pedis=redis.StrictRedis(host=redisHost, port=6379, charset="utf-8", decode_responses=True)
        dry=False
        
        for exp in range(1):
            #here we assume that redis and mongo are on the same host
            sys = nodeSys(dbHost=redisHost)
            pedis.flushall();
            
            #init CPU allocation in the case of simulated CPU
            pedis.mset({"MSauth_hw":"3.6572",
                        "MSvalidateid_hw":"1.8773",
                        "MSbookflights_hw":"3.1551", 
                        "MSupdateMiles_hw":"5.0964",
                        "MScancelbooking_hw":"2.0323", 
                        "MSgetrewardmiles_hw":"4.3805",
                         "MSqueryflights_hw":"6.4983",
                         "MSviewprofile_hw":"3.5825",
                         "MSupdateprofile_hw":"2.7341" })
            
            #start the controller
            ctrl=getCtrl(args.ctrl,args.load)
            sys.startCtrl(ctrl,pedis)
            print("ctrl started")
            
            datadir="../data/replication/%s_%d/"%(ctrl["name"],exp)
            os.makedirs( datadir, exist_ok=True)
            
            initUsr=10
            #lancio i client iniziali
            sys.startClient(initUsr,dry=dry)
            startLoadShape(args.load)
            
            pedis.set("users","%d"%(1))
            pedis.publish("users","%d"%(1))  
            
            setStart(pedis)
            waitExp(pedis)
            
            print("killing clients")
            sys.stopClient()
            print("killing ctrl")
            sys.ctrlProc.kill()
            subprocess.call(["pkill","-9","-f","matlab"])
            subprocess.call(["pkill","-9","-f","julia"])
    
    except Exception as ex:
        print("Error")
        print("killing clients")
        sys.stopClient()
        print("killing ctrl")
        sys.ctrlProc.kill()
        subprocess.call(["pkill","-9","-f","matlab"])
        subprocess.call(["pkill","-9","-f","julia"])

        
        traceback.print_exception(type(ex), ex, ex.__traceback__)
        
