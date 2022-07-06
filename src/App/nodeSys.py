import requests as req
import subprocess
import time
import psutil
from Client import clientThread
from Monitoring import mnt_thread
from pymongo import MongoClient
import pymongo

class nodeSys():
    
    #oggetto che rappresenta il sistema, immagino che sia un array di oggetti, che contenga come attributi
    #indirizzo, porta, nome
    nodeSys=None
    #mappa con la stessa struttura di prima ma che contiene i processi node del sistema
    nodeSysProc=None
    clientThreads=None
    mntThreads=None
    data=None
    startTime=None
    
    def __init__(self,nodeSys):
        self.nodeSys=nodeSys
        self.nodeSysProc={}
        self.clientThreads=[]
        self.mntThreads=[]
        self.data={}
        self.startTime=None
    
    
    def startSys(self):
        for ms in self.nodeSys:
            msOutf = open("../log/%sOut.log"%(ms), "w+")
            msErrf = open("../log/%sErr.log"%(ms), "w+")
        
            self.nodeSysProc[ms]=subprocess.Popen(["node", self.nodeSys[ms]["appFile"],"ms_name=%s"%(ms),
                                                   "port=%s"%(self.nodeSys[ms]["port"]),
                                                   "mnt_port=%s"%(self.nodeSys[ms]["mntPort"])], 
                                                  stdout=msOutf, stderr=msErrf)
            self.waitMs(ms)
            
            msOutf.close()
            msErrf.close()
    
    def stopSys(self):
        for ms in self.nodeSysProc:
            self.nodeSysProc[ms].terminate()
            try:
                self.nodeSysProc[ms].wait(timeout=2)
            except psutil.TimeoutExpired as e:
                self.nodeSysProc[ms].kill()
    
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
            self.clientThreads.append(clientThread(ttime=500))
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
                r = req.get("http://%s:%d/0"%(self.nodeSys[msName]["addr"],self.nodeSys[msName]["mntPort"]))
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
        for ms in self.nodeSys:
            self.mntThreads.append(mnt_thread(self.nodeSys[ms],1.,ms,self.startTime))
            self.mntThreads[-1].start()
        
        self.mntThreads.append(mnt_thread({"Client":{}},1.,"client",self.startTime))
        self.mntThreads[-1].start()
    
        for t in self.mntThreads:
            t.join()
            
            d=t.getData()
            self.data[t.name]={"rt":d[0],"tr":d[1]}
        
        
    def reset(self):
        clientThread.toStop=False
        clientThread.id=0
        
        self.nodeSysProc={}
        self.clientThreads=[]
        self.mntThreads=[]
        self.data={}
        self.startTime=None
    
    
    
    