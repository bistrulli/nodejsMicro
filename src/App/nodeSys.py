import requests as req
import subprocess
import time
import psutil
from Client import clientThread
from Monitoring import mnt_thread
from pymongo import MongoClient
import pymongo
from utility import CountDownLatch 
import shutil
import os

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
    
    def __init__(self,nodeSys):
        self.nodeSys=nodeSys
        self.nodeSysProc={}
        self.nodePrxProc={}
        self.clientThreads=[]
        self.mntThreads=[]
        self.data={}
        self.startTime=None
        #self.clearLog()
    
    
    def startSys(self):
        for ms in self.nodeSys:
            msOutf = open("../log/%sOut.log"%(ms), "w+")
            msPrxOutf = open("../log/%sPrxOut.log"%(ms), "w+")
            msErrf = open("../log/%sErr.log"%(ms), "w+")
            msPrxErrf = open("../log/%sPrxErr.log"%(ms), "w+")
            
            # self.nodePrxProc[ms]=subprocess.Popen(["node", self.nodeSys[ms]["prxFile"],"port=%s"%(self.nodeSys[ms]["prxPort"]),
            #                                        "tgtPort=%s"%(self.nodeSys[ms]["port"])], 
            #                                       stdout=msPrxOutf, stderr=msPrxErrf)
            
            self.nodePrxProc[ms]=subprocess.Popen(["java","-jar",self.nodeSys[ms]["prxFile"],
                                                   "--tgtPort","%d"%self.nodeSys[ms]["port"]
                                                   ,"--prxPort","%d"%self.nodeSys[ms]["prxPort"]], 
                                      stdout=msPrxOutf, stderr=msPrxErrf)
            
            self.nodeSysProc[ms]=subprocess.Popen(["node",self.nodeSys[ms]["appFile"],"ms_name=%s"%(ms),
                                                   "port=%s"%(self.nodeSys[ms]["port"])], 
                                                  stdout=msOutf, stderr=msErrf)
            self.waitMs(ms)
            
            msOutf.close()
            msPrxOutf.close()
            msErrf.close()
            msPrxErrf.close()
    
    def stopSys(self):
        for ms in self.nodeSysProc:
            self.nodeSysProc[ms].terminate()
            try:
                self.nodeSysProc[ms].wait(timeout=2)
            except psutil.TimeoutExpired as e:
                self.nodeSysProc[ms].kill()
        
        for ms in self.nodePrxProc:
            self.nodePrxProc[ms].terminate()
            try:
                self.nodePrxProc[ms].wait(timeout=2)
            except psutil.TimeoutExpired as e:
                self.nodePrxProc[ms].kill()
    
    def startClient(self,N):
        
        client=MongoClient("mongodb://localhost:27017/client")
        try:
            client["client"]["rt"].drop()
        except:
            pass
        finally:
            client["client"].create_collection("rt")
        
        self.startTime=time.time_ns() // 1_000_000 
        for n in range(N):
            self.clientThreads.append(clientThread(ttime=200))
            self.clientThreads[-1].start()
    
    def stopClient(self):
        clientThread.toStop=True
        for c in self.clientThreads:
            c.join()
            print("stopped client %d"%(c.id))
    
    def waitMs(self,msName):
        atpt = 0
        limit = 10
        connected = False
        r=None
        while(atpt < limit and not connected):
            try:
                r = req.get("http://%s:%d/mnt"%(self.nodeSys[msName]["addr"],self.nodeSys[msName]["port"]))
                connected = True
                break
            except:
                time.sleep(0.2)
            finally:
                atpt += 1
        
        if(connected):
            print("connected to %s"%(msName))
        else:
            raise ValueError("error while connceting %s"%(msName))
        
    
    def startMNT(self):
        latch=CountDownLatch(len(self.nodeSys)+1)
        
        self.mntThreads.append(mnt_thread({"Client":{}},1.,"client",self.startTime,countDown=latch))
        self.mntThreads[-1].start()
        
        for ms in self.nodeSys:
            self.mntThreads.append(mnt_thread(self.nodeSys[ms],1.,ms,self.startTime,countDown=latch))
            self.mntThreads[-1].start()
    
        for t in self.mntThreads:
            t.join()
            
            d=t.getData()
            self.data[t.name]={"rt":d[0],"tr":d[1]}
    
    def clearLog(self):
        shutil.rmtree('../log')
        os.makedirs('../log')
        
        
    def reset(self):
        clientThread.toStop=False
        clientThread.id=0
        
        self.nodeSysProc={}
        self.clientThreads=[]
        self.mntThreads=[]
        self.data={}
        self.startTime=None
    
    
    
    