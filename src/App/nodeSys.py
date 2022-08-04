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
import socket
import numpy as np
import json
import glob

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
        self.clearLog()
    
    
    def startSys(self):
        
        mongoCli=MongoClient("mongodb://localhost:27017/sys")
        try:
            mongoCli["sys"]["ms"].drop()
        except:
            pass
        finally:
            mongoCli["sys"].create_collection("ms")
        
        for ms in self.nodeSys:
            
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
                self.nodeSysProc[ms]+=[subprocess.Popen(["node",
                                                         # "--min_semi_space_size=2000",
                                                         # "--max_semi_space_size=2000",
                                                         # "--initial_old_space_size=2000",
                                                         # "--max_old_space_size=2000",
                                                         # "--scavenge_task",
                                                         "--v8-pool-size=8",
                                                         self.nodeSys[ms]["appFile"],"ms_name=%s"%(ms),
                                                       "port=%s"%(port)], 
                                                      stdout=msOutf, stderr=msErrf)]
                self.waitMs(ms,port)
                
                msOutf.close()
                msErrf.close()
            
           
            msPrxOutf = open("../log/%sPrxOut.log"%(ms), "w+")
            msPrxErrf = open("../log/%sPrxErr.log"%(ms), "w+")
            
            self.nodeSys[ms]["prxPort"]=self.getRandomPort()
            self.nodePrxProc[ms]=subprocess.Popen(["java",
                                                   "-Xmx6g",
                                                   "-jar",self.nodeSys[ms]["prxFile"]
                                                   ,"--prxPort","%d"%(self.nodeSys[ms]["prxPort"]),
                                                   "--msName","%s"%(ms)],
                                                   stdout=msPrxOutf, stderr=msPrxErrf)
            
            msPrxOutf.close()
            msPrxErrf.close()
            
            #salvo le informazioni di questo microservizio
            self.nodeSys[ms]["name"]=ms;
            mongoCli["sys"]["ms"].insert_one(self.nodeSys[ms])
            
    
    def stopSys(self):
        for ms in self.nodeSysProc:
            for p in self.nodeSysProc[ms]:
                p.terminate()
                try:
                    p.wait(timeout=2)
                except psutil.TimeoutExpired as e:
                    p.kill()
        
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
    
    def waitMs(self,msName=None,port=None):
        atpt = 0
        limit = 10
        connected = False
        r=None
        while(atpt < limit and not connected):
            try:
                r = req.get("http://%s:%d/mnt"%(self.nodeSys[msName]["addr"],port))
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
    
    def is_port_in_use(self,port: int) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            res=s.connect_ex(('localhost', port))
            if(res==0):
                s.close()
                return res
            
    
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
        
        
    def reset(self):
        clientThread.toStop=False
        clientThread.id=0
        
        self.nodeSysProc={}
        self.clientThreads=[]
        self.mntThreads=[]
        self.data={}
        self.startTime=None
    
    
    
    