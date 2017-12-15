# -*- coding: utf-8 -*-
from novaclient import client
import client_setting
import globalFunction as gf
import sys
import io
import os
# from multiprocessing.pool import ThreadPool
import time
from threading import Thread

argv = sys.argv[1]
VM_UUID = sys.argv[2]
is_snapshotclone = sys.argv[3]
host_uuid =  sys.argv[4] # host id
sruuid = sys.argv[5]
serverip = sys.argv[6]
serveraccount = sys.argv[7]
serverpwd = sys.argv[8]
pool_name = sys.argv[9]
operator =sys.argv[10]
guid = sys.argv[11]
ProjectName= sys.argv[12]

nova = client_setting.nova(serverip,serveraccount,serverpwd,ProjectName)
servers = nova.servers
sl = servers.list()

def dynstart():
	vm = servers.get(VM_UUID)
	# print dir(vm)
	# print(vm.status)
	if vm.status == 'PAUSED':
	    vm.unpause()
	elif vm.status == 'SUSPENDED':
		vm.resume()
	return 1

def scan_vm():
    #servers define
    def checkStatus(vmid):
       while True:
           time.sleep(1)
           if servers.get(vmid).status == "ACTIVE":
               return servers.get(vmid).status
       	       break
    class ThreadWithReturnValue(Thread):
        def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
            Thread.__init__(self, group, target, name, args, kwargs, Verbose)
            self._return = None
        def run(self):
            if self._Thread__target is not None:
                self._return = self._Thread__target(*self._Thread__args,
                                                **self._Thread__kwargs)
        def join(self):
            Thread.join(self)
            return self._return

    output = "" 
    for item in sl:
        
        VM_UUID = item.id
        VM_Name = item.name

        ip_array=[]
        for n in item.networks: #取得network name
            for ip in item.networks[n]: #用network name 去取得IP
                ip_array.append(ip)
                
        VM_IP=ip_array
        #
        twrv = ThreadWithReturnValue(target=checkStatus, args=(VM_UUID,))
        twrv.start()
        VM_Status = twrv.join()
        Host_UUID = item.hostId
       
        item_array={'VM_UUID':item.id,'VM_Name':item.name,'VM_IP':VM_IP,'VM_Status':VM_Status,'Host_UUID':Host_UUID}
        output += str(item_array)+"\n"
    return output



if __name__ == '__main__':
	dynstart()
	#f = open('C://eDC/Cmd/'+guid+'.txt', 'a')
	f = open(guid+'.txt', 'a')
	f.write('[vm]\n')
	f.write(scan_vm())
	f.write('[END]\n')
	f.close()
