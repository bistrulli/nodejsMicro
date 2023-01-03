import requests as req
import numpy as np
from Client import clientProcess
import json
import traceback


class clientProcess_sock(clientProcess):
    
    def __init__(self, ttime,id):
        super().__init__(ttime,id)
        
    def userLogic(self):
        try:
            # s = req.Session()
            #
            # adapter = req.adapters.HTTPAdapter(pool_connections=200, pool_maxsize=200)
            # s.mount('http://', adapter)
            #
            # data = {"login":"uid0@email.com",
            #         "password":"password"}
            #
            # r = s.post(url="http://localhost:80/auth/login", data=data)
            # # print("login req", r)
            # # print(r.text)
            # r = s.get(url="http://localhost:80/customer/byid/%s" % (data["login"]), data={})
            # # print("view profile req", r)
            # # print(r.text)
            #
            # userData = json.loads(r.text);
            # number = "".join(map(str, np.random.randint(low=0, high=9, size=9)))
            # userData["phoneNumber"] = number
            # userData["password"] = data["password"];
            # r = s.post(url="http://localhost:80/customer/byid/%s" % (data["login"]), headers={"Content-Type": "application/json; charset=utf-8"},
            #          json=userData)
            # # print("update profile req", r)
            # # print(r.text)
            # userData = json.loads(r.text);
            # r = s.get(url="http://localhost:80/customer/byid/%s" % (data["login"]), data={})
            # # print("view profile req2", r)
            # # print(r.text)
            #
            # # query flight
            # queryData = {"fromAirport": "FCO",
            #             "toAirport": "LHR",
            #             "fromDate": "Fri Sep 02 2022 00:00:00 GMT+0200 (Ora standard dell’Europa centrale)",
            #             "returnDate": "Sat Sep 03 2022 00:00:00 GMT+0200 (Ora standard dell’Europa centrale)",
            #             "oneWay": False}
            # r = s.post(url="http://localhost:80/flight/queryflights", data=queryData)
            #
            # flightData = json.loads(r.text);
            # # print(flightData)
            #
            # # book flight
            # toFlight = flightData["tripFlights"][0]["flightsOptions"][0]
            # retFlight = flightData["tripFlights"][1]["flightsOptions"][0]
            # bookingData = {
            #           "userid": userData["_id"],
            #           "toFlightId": toFlight["_id"],
            #           "toFlightSegId": toFlight["flightSegmentId"],
            #           "retFlightId": retFlight["_id"],
            #           "retFlightSegId": retFlight["flightSegmentId"],
            #           "oneWayFlight": False
            #     }
            # r = s.post(url="http://localhost:80/booking/bookflights", data=bookingData)
            # # print("booking")
            # bookingRes = json.loads(r.text)
            # # print(bookingRes)
            #
            # # cancel booking
            # bookToCancel = {"userid": userData["_id"],
            #                 "number": bookingRes["departBookingId"]}
            # r = s.post(url="http://localhost:80/booking/cancelbooking", data=bookToCancel)
            # # print(r.text)
            # bookToCancel["number"] = bookingRes["returnBookingId"]
            # r = s.post(url="http://localhost:80/booking/cancelbooking", data=bookToCancel)
            # # print(r.text)
            #
            # s.close()
            
            s = req.Session()
            adapter = req.adapters.HTTPAdapter(pool_connections=200, pool_maxsize=200)
            s.mount('http://', adapter)
            
            print("login")
            r=s.get(url="http://localhost/login",auth=("Eve_Berger", "eve"))
            #print(r.text)
            
            print("view profile")
            r=s.get(url="http://localhost/customers/Eve_Berger")
            #print(r.text)
            
            print("view cutomer cards")
            r=s.get(url="http://localhost/customers/Eve_Berger/cards")
            cards=json.loads(r.text)
            print(len(cards["_embedded"]["card"]))
            
            #qui aggiungere un po di chiamate per la ricerca, acquisto e checkout di un prodotto
            
            # print("add cards")
            # cardsData = {
            #           "longNum": "19394949272",
            #           "expires": "01/01/2023",
            #           "ccv": "123",
            #           "userID":"Eve_Berger"
            #     }            
            # r = s.post(url="http://localhost/cards",headers={"Content-Type": "application/json; charset=utf-8"},
            #            data=json.dumps(cardsData))
            # print(r,r.text)
            
            # print("view cutomer cards")
            # r=s.get(url="http://localhost/customers/Eve_Berger/cards")
            # print(r.text)
            
            print("view cutomer addresses")
            r=s.get(url="http://localhost/customers/Eve_Berger/addresses")
            #print(r,r.text)
            
            #print("view cutomer cards")
            #r = s.get(url="http://localhost/catalogue")
            
            
            
        except Exception as ex:
            # print(self.id, "error")
            # pass
            traceback.print_exception(type(ex), ex, ex.__traceback__)
    
    
