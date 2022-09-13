import requests as req
import numpy as np
import time
from threading import Thread
from pymongo import MongoClient
import pymongo
from Client import clientThread
import json


class clientThread_acme(clientThread):
    
    def __init__(self,ttime):
        super().__init__(ttime)
    
    def run(self):
        while(not clientThread.toStop):
            #qui metto la logica per recuperare un utente random
            try:
                st = time.time_ns() // 1_000_000 
                self.think()
                
                s = req.Session()
                data = {"login":"uid0@email.com",
                        "password":"password"}
    
                r = s.post(url="http://localhost:80/auth/login",data=data)
                print("login req",r)
                print(r.text)
                r=s.get(url="http://localhost/customer/byid/%s"%(data["login"]),data={})
                print("view profile req",r)
                print(r.text)
                
                userData=json.loads(r.text);
                number="".join(map(str,np.random.randint(low=0,high=9,size=9)))
                userData["phoneNumber"]=number
                userData["password"]=data["password"];
                r=s.post(url="http://localhost/customer/byid/%s"%(data["login"]),headers={"Content-Type": "application/json; charset=utf-8"},
                         json=userData)
                print("update profile req",r)
                print(r.text)
                userData=json.loads(r.text);
                r=s.get(url="http://localhost/customer/byid/%s"%(data["login"]),data={})
                print("view profile req2",r)
                print(r.text)
                
                s.close()
                
                end= time.time_ns() // 1_000_000
                self.mongoClient["client"]["rt"].insert_one({"st":st,"end":end})
            except:
                print(self.id,"error")
                pass
    
    