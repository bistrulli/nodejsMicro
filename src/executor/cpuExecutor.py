from threading import Thread
import subprocess
import redis
import time

class CPUExecutor(Thread):
    msname=None
    cfs_period_us  =  100000
    cfs_quota_us = None
    rediscon=None
    toStop=False
    
    def __init__(self, msnae,redisHpst="localhost",redisPort=6379):
        Thread.__init__(self)
        self.msname=msnae
        self.rediscon=redis.StrictRedis(host=redisHpst, port=redisPort, charset="utf-8", decode_responses=True)
       
    def run(self):
        while(not CPUExecutor.toStop):
            cores=float(self.rediscon.get("%s_hw"%(self.msname)))
            self.cfs_quota_us=cores*self.cfs_period_us
            subprocess.call(["sudo","cgset","-r","cpu.cfs_quota_us=%d"%(int(self.cfs_quota_us)),"%s"%(self.msname)])
            time.sleep(1)