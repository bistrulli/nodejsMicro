from pymongo import MongoClient
import pymongo
import numpy as np
import time

# ms3Client = MongoClient("mongodb://localhost:27017/ms3")
# cursorMs3 = ms3Client["ms3"]["rt"].count_documents({})

ms2Client = MongoClient("mongodb://localhost:27017/ms2")
ms1Client = MongoClient("mongodb://localhost:27017/ms1")
driverClient = MongoClient("mongodb://localhost:27017/client")

while(True):
    nms2 = ms2Client["ms2"]["rt"].count_documents({})
    nms1 = ms1Client["ms1"]["rt"].count_documents({})
    nclient = driverClient["client"]["rt"].count_documents({})
    
    print([nms2,nms1,nclient])
    
    time.sleep(0.2)
    
    
    

# rtData1=[]
# for item in cursorMs3:
#     rtData1.append(int(item["end"]) - int(item["st"]))
#
# rtData2=[]
# for item in cursorMs2:
#     rtData2.append(int(item["end"]) - int(item["st"]))
#
# rtData3=[]
# for item in cursorMs1:
#     rtData3.append(int(item["end"]) - int(item["st"]))
#
# rtData4=[]
# for item in cursorClient:
#     rtData4.append(int(item["end"]) - int(item["st"]))
#
#
#
# print("ms3",np.mean(rtData1),np.min(rtData1),np.max(rtData1))
# print("ms2",np.mean(rtData2),np.min(rtData2),np.max(rtData2))
# print("ms1",np.mean(rtData3),np.min(rtData3),np.max(rtData3))
# print("client",np.mean(rtData4),np.min(rtData4),np.max(rtData4))
