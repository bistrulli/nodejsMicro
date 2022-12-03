import requests as req
import subprocess
import time
import psutil
from Client import clientThread
from Client import clientProcess_acme
from Client import loadShapeAcme_step
from Monitoring import mnt_thread
from pymongo import MongoClient
import pymongo
from utility import CountDownLatch 
import shutil
import os
import socket
import numpy as np
import glob
import copy
import traceback
import tempfile
import re
from queue import Queue

class nodeSys():
    
    #oggetto che rappresenta il sistema, immagino che sia un array di oggetti, che contenga come attributi
    #indirizzo, porta, nome
    nodeSys=None
    #mappa con la stessa struttura di prima ma che contiene i processi node del sistema
    nodeSysProc=None
    nodePrxProc=None
    clientThreads=None
    mntThreads=None
    data=None
    startTime=None
    clientsProc=None
    userCount=None
    userId=0
    
    def __init__(self):
        self.nodeSysProc={}
        self.nodePrxProc={}
        self.clientThreads=[]
        self.mntThreads=[]
        self.data={}
        self.startTime=None
        self.clientsProc=Queue()
        nodeSys.userId=0
        self.userCount=0
        #self.clearLog()
    
    
    def startSys(self,msSys=None):
        
        self.nodeSys=copy.deepcopy(msSys)
        
        mongoCli=MongoClient("mongodb://localhost:27017/") 
        try:
            mongoCli.drop_database("sys")
        except:
            pass
        finally:
            mongoCli["sys"].create_collection("ms")
        
        for ms in self.nodeSys:
            if(type(self.nodeSys[ms])==dict and "type" in self.nodeSys[ms]):
                port=None
                for rep in range(self.nodeSys[ms]["replica"]):
                    port=self.getRandomPort()
                    msOutf = open("../log/%sOut_%d.log"%(ms,port), "w+")
                    msErrf = open("../log/%sErr_%d.log"%(ms,port), "w+")
                    
                    if(not ms in self.nodeSysProc):
                        self.nodeSysProc[ms]=[]
                    if(not "ports" in self.nodeSys[ms]):
                        self.nodeSys[ms]["ports"]=[]
                    
                    self.nodeSys[ms]["ports"]+=[port]
                    
                    if(self.nodeSys[ms]["type"]=="node"):
                        self.nodeSysProc[ms]+=[subprocess.Popen(["node",
                                                                 "--min_semi_space_size=2000",
                                                                 "--max_semi_space_size=2000",
                                                                 "--initial_old_space_size=2000",
                                                                 "--max_old_space_size=2000",
                                                                 "--scavenge_task",
                                                                 "--v8-pool-size=8",
                                                                 self.nodeSys[ms]["appFile"],"ms_name=%s"%(ms),
                                                               "port=%s"%(port)], 
                                                              stdout=msOutf, stderr=msErrf)]
                    elif(self.nodeSys[ms]["type"]=="spring"):
                        self.nodeSysProc[ms]+=[subprocess.Popen(["java","-jar",
                                                                 "-Xmx10g",
                                                                 self.nodeSys[ms]["appFile"],"ms_name=%s"%(ms),
                                                                 "--server.port=%d"%(port),
                                                                 "--ms.name=%s"%(ms),
                                                                 "--ms.hw=%f"%(self.nodeSys[ms]["hw"])], 
                                                              stdout=msOutf, stderr=msErrf)]
                        
                    self.waitMs(ms,port)
                    
                    msOutf.close()
                    msErrf.close()
            
           
                self.nodeSys[ms]["prxPort"]=self.getRandomPort()
                msPrxOutf = open("../log/%sPrxOut_%d.log"%(ms,self.nodeSys[ms]["prxPort"]), "w+")
                msPrxErrf = open("../log/%sPrxErr_%d.log"%(ms,self.nodeSys[ms]["prxPort"]), "w+")
                
                self.nodePrxProc[ms]=subprocess.Popen(["java",
                                                       "-Xmx10g",
                                                       "-jar",self.nodeSys[ms]["prxFile"]
                                                       ,"--prxPort","%d"%(self.nodeSys[ms]["prxPort"]),
                                                       "--msName","%s"%(ms)],
                                                       stdout=msPrxOutf, stderr=msPrxErrf)
                
                msPrxOutf.close()
                msPrxErrf.close()
                
                #salvo le informazioni di questo microservizio
                self.nodeSys[ms]["name"]=ms;
                mongoCli["sys"]["ms"].insert_one(self.nodeSys[ms])
            
        #se sto valutando acmeair allora lancio il proxy con la configurazione opportuna
        #--> in base alle porte generate genero il template della cofigurazione
        #--> lancio haproxy dovrebbe funzioanre tutto
        
        if("acmeair" in self.nodeSys and self.nodeSys["acmeair"]):
            #sto valutando acmeair
            cfg=self.updateHaPrxPort()
            self.startHaPrx(cfg);
                
            
    
    def stopSys(self):
        for ms in self.nodeSysProc:
            for p in self.nodeSysProc[ms]:                
                print("killing proc",ms,p.pid)
                pU = psutil.Process(p.pid)
                pU.kill()
        
        for ms in self.nodePrxProc:
            print("killing Prx Proc",ms,self.nodePrxProc[ms].pid)
            p=psutil.Process(self.nodePrxProc[ms].pid)
            p.kill()
            
    
    def startClient(self,N):
        
        print("starting client")
        
        client=MongoClient("mongodb://localhost:27017/client")
        try:
            client["client"]["rt"].drop()
        except:
            pass
        finally:
            client["client"].create_collection("rt")
        
        self.startTime=time.time_ns() // 1_000_000 
        self.addUsers(N)
        
    
    
    def addUsers(self,nusers):
        for i in range(nusers):
            u=clientProcess_acme(ttime=200,id=self.userId)
            self.clientsProc.put(u)
            u.start()
            self.userCount+=1
            self.userId+=1
    
    def stopUsers(self,nusers):
        if(nusers>self.clientsProc.qsize()):
            raise ValueError("less users than what required")
        for uIdx in range(nusers):
            u=self.clientsProc.get()
            u.terminate()
            u.join()
            print("stopped client %d"%(u.id))
            
    
    def stopClient(self):
        self.stopUsers(self.clientsProc.qsize())
            
    def startLoadShape(self,maxt):
        lshape=loadShapeAcme_step(maxt=maxt,sys=self)
        lshape.start()
    
    def waitMs(self,msName=None,port=None):
        atpt = 0
        limit = 60
        connected = False
        r=None
        while(atpt < limit and not connected):
            try:
                r = req.get("http://%s:%d/"%(self.nodeSys[msName]["addr"],port))
                connected = True
                r.close()
                break
            except:
                time.sleep(1.0)
            finally:
                atpt += 1
        
        if(connected):
            print("connected to %s"%(msName))
        else:
            raise ValueError("error while connceting %s"%(msName))
        
    
    def startMNT(self):
        nms=0
        for ms in self.nodeSys:
            if(type(self.nodeSys[ms])==dict and "type" in self.nodeSys[ms]):
                nms+=1
        
        latch=CountDownLatch(nms+1)
        
        self.mntThreads.append(mnt_thread({"Client":{}},1.,"client",self.startTime,countDown=latch))
        self.mntThreads[-1].start()
        
        for ms in self.nodeSys:
            if(type(self.nodeSys[ms])==dict and "type" in self.nodeSys[ms]):
                self.mntThreads.append(mnt_thread(self.nodeSys[ms],1.,ms,self.startTime,countDown=latch))
                self.mntThreads[-1].start()
    
        for t in self.mntThreads:
            t.join()
            
            d=t.getData()
            self.data[t.name]={"rt":d[0],"tr":d[1]}
    
    def is_port_in_use(self,port: int) -> bool:
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        inUse=None
        try:
            s.bind(('', port))
            s.close()
            inUse=False
        except OSError:
            inUse=True
        return inUse
        
    
    def getRandomPort(self) -> int:
        port=np.random.randint(low=3000,high=65535)
        while(self.is_port_in_use(port)):
            port=np.random.randint(low=3000,high=65535)
        return port
    
    def clearLog(self):
        files = glob.glob('../log/*.log')
        for f in files:
            try:
                os.remove(os.path.abspath(f))
            except OSError as e:
                print("Error: %s : %s" % (f, e.strerror))
                
    
    def updateHaPrxPort(self):
        cfgfile=open("../cfgTmp/acmeair.cfg","r")
        cfg = cfgfile.read()
        cfgfile.close()
        
        for ms in self.nodeSys:
            if(type(self.nodeSys[ms])==dict and "type" in self.nodeSys[ms]):
                cfg = re.sub(r"\$%s"%(ms), str(self.nodeSys["%s"%(ms)]["prxPort"]),str(cfg))
        
        # cfgFile = tempfile.NamedTemporaryFile(suffix='.cfg',mode='w+', encoding='utf-8')
        # f=open(cfgFile.name,"w")
        # f.write(cfg)
        # f.close()
        
        cfgFile=open("../log/ha.cfg","w")
        cfgFile.write(cfg)
        cfgFile.close()
        
        return cfgFile
        
    
    def startHaPrx(self,cfgFile):
        haOutf = open("../log/haOut.log", "w+")
        haErrf = open("../log/haErr.log", "w+")
        
        self.nodePrxProc["haPrx"]=subprocess.Popen(["haproxy","-f",os.path.abspath(cfgFile.name)], 
                                                    stdout=haOutf, stderr=haErrf)
        
        print("started HaProxy")
        
    def reset(self):
        clientThread.toStop=False
        clientThread.i=0
        
        self.nodeSys={}
        self.nodeSysProc={}
        self.clientThreads=[]
        self.mntThreads=[]
        self.data={}
        self.startTime=None
        self.clearLog()
    
    
    
    
