import time
import traceback
import redis
from App import nodeSys
import os
from pymongo import MongoClient
import subprocess
import argparse


def getCliOptions():
    parser = argparse.ArgumentParser(description='muOpt Experiments Runner')
    parser.add_argument('ctrl', choices=['muopt', 'atom'],help='specify the controller to use')
    parser.add_argument("load",choices=["step_slow","sin","step",'tweeter_7_8',"wc98"],help='specify the load shape to use')
    args = parser.parse_args()
    return args


def extractKPI(msname,datadir):
    subprocess.check_call(["mongoexport","-d",msname,"-c","rt","-f","st,end","--type=csv","-o","%s/%s.csv"%(datadir,msname)]);

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

def getCtrl(ctrlName,loadName):
    ctrl=None
    if(ctrlName=="muopt"):
        ctrl={"name":"julia_%s"%(loadName),"workDir":"/home/virtual/git/atom-replication/LQN-CRN/controller/acmeAir/",
          "ctrlCmd":"julia acmeCtrl.jl"}
    elif(ctrlName=="atom"):
        ctrl={"name":"atom_%s"%(loadName),"workDir":"/home/virtual/git/atom-replication/GA/",
         "ctrlCmd":"matlab -nodesktop -nosplash -nodisplay -nojvm -r main(3) quit;"}
        
    return ctrl
    


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
        
        
        #here the host where redis is installed
        redisHost="127.0.0.1"
        msNames=list(msSys.keys());
        pedis=redis.StrictRedis(host=redisHost, port=6379, charset="utf-8", decode_responses=True)
        dry=False
        
        for exp in range(1):
            
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
            
            
            ctrl=getCtrl(args.ctrl,args.load)
            datadir="../data/replication/%s_%d/"%(ctrl["name"],exp)
            os.makedirs( datadir, exist_ok=True)
            
            print("starting Acmeair")
            sys.startSys(msSys=msSys)
            time.sleep(5)
            print("sys started")
            
            #wait the end of the experiment
            waitExp(pedis) 
            
            if(not dry):
                for ms in list(msSys.keys()):
                    if(ms=="acmeair"):
                        continue
                    
                    print("saving",ms)
                    extractKPI(ms,datadir)
                extractKPI("client",datadir)
                
            print("killing system") 
            sys.stopSys()
            sys.reset()
            resetSim()
            sys.clearLog()
    
    except Exception as ex:
        print("Error")
        print("killing system") 
        sys.stopSys()
        resetSim()
        
        traceback.print_exception(type(ex), ex, ex.__traceback__)
        
