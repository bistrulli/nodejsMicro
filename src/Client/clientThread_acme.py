import requests as req
import numpy as np
import time
from threading import Thread
from pymongo import MongoClient
import pymongo
from Client import clientThread
import json


class clientThread_acme(clientThread):
    
    def __init__(self, ttime):
        super().__init__(ttime)
    
    def run(self):
        while(not clientThread.toStop):
            # qui metto la logica per recuperare un utente random
            try:
                st = time.time_ns() // 1_000_000 
                self.think()
                
                s = req.Session()
                
                adapter = req.adapters.HTTPAdapter(pool_connections=200, pool_maxsize=200)
                s.mount('http://', adapter)
                
                data = {"login":"uid0@email.com",
                        "password":"password"}
    
                r = s.post(url="http://localhost:80/auth/login", data=data)
                #print("login req", r)
                #print(r.text)
                r = s.get(url="http://localhost/customer/byid/%s" % (data["login"]), data={})
                #print("view profile req", r)
                #print(r.text)
                
                userData = json.loads(r.text);
                number = "".join(map(str, np.random.randint(low=0, high=9, size=9)))
                userData["phoneNumber"] = number
                userData["password"] = data["password"];
                r = s.post(url="http://localhost/customer/byid/%s" % (data["login"]), headers={"Content-Type": "application/json; charset=utf-8"},
                         json=userData)
                #print("update profile req", r)
                #print(r.text)
                userData = json.loads(r.text);
                r = s.get(url="http://localhost/customer/byid/%s" % (data["login"]), data={})
                #print("view profile req2", r)
                #print(r.text)
                
                # query flight
                queryData = {"fromAirport": "FCO",
                            "toAirport": "LHR",
                            "fromDate": "Fri Sep 02 2022 00:00:00 GMT+0200 (Ora standard dell’Europa centrale)",
                            "returnDate": "Sat Sep 03 2022 00:00:00 GMT+0200 (Ora standard dell’Europa centrale)",
                            "oneWay": False}
                r = s.post(url="http://localhost/flight/queryflights", data=queryData)
            
                flightData = json.loads(r.text);
                #print(flightData)
                                      
                # book flight
                toFlight = flightData["tripFlights"][0]["flightsOptions"][0]
                retFlight = flightData["tripFlights"][1]["flightsOptions"][0]
                bookingData = {
                          "userid": userData["_id"],
                          "toFlightId": toFlight["_id"],
                          "toFlightSegId": toFlight["flightSegmentId"],
                          "retFlightId": retFlight["_id"],
                          "retFlightSegId": retFlight["flightSegmentId"],
                          "oneWayFlight": False
                    }
                r = s.post(url="http://localhost/booking/bookflights", data=bookingData)
                #print("booking")
                bookingRes = json.loads(r.text)
                #print(bookingRes)
                
                # cancel booking
                bookToCancel = {"userid": userData["_id"],
                                "number": bookingRes["departBookingId"]}
                r = s.post(url="http://localhost/booking/cancelbooking", data=bookToCancel)
                #print(r.text)
                bookToCancel["number"] = bookingRes["returnBookingId"]
                r = s.post(url="http://localhost/booking/cancelbooking", data=bookToCancel)
                #print(r.text)
                
                s.close()
                
                end = time.time_ns() // 1_000_000
                self.mongoClient["client"]["rt"].insert_one({"st":st, "end":end})
            except:
                print(self.id, "error")
                pass
    
