# -*- coding: utf-8 -*-
import time
import random
from itertools import chain

def getTime():
	now = int(time.time())
	return now



class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False
 
    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration
     
    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False

def compareHost(serverip,serveraccount,serverpwd,projectname):
	import client_setting
	nova = client_setting.nova(serverip,serveraccount,serverpwd,projectname)
	maxHost =""
	maxFreeMemory = 0
	for item in nova.hypervisors.list():
		#比較所有status 為 enabled的host的free memory,取最高的
		if item.status == "enabled":
			if item.free_ram_mb > maxFreeMemory:
				maxFreeMemory=item.free_ram_mb
				maxHost = item.hypervisor_hostname

	return maxHost
	
def createRamdom():
    list = ['0','1', '2', '3', '4', '5', '6', '7', '8', '9','a','b','c','d','e','f']
    s1 = random.sample(list, 8)
    s2 = random.sample(list, 4)
    s3 = random.sample(list, 4)
    s4 = random.sample(list, 4)
    s5 = random.sample(list, 12)
    d=['-']
    s = chain.from_iterable([s1,d,s2,d,s3,d,s4,d,s5])
    tmpString = ""
    for i in s:
        tmpString+=i
    return tmpString
