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

#python Snapshotvm.py 28b904d6-6c82-4f90-ae9e-9cc392f83a2c 140.128.101.205 admin 1j6el4nj4su3 admin 0 snapshot
vm_uuid = sys.argv[1]
serverip = sys.argv[2]
serveraccount = sys.argv[3]
serverpwd = sys.argv[4]
poolname = sys.argv[5]
operator =sys.argv[6]
guid = sys.argv[7]
projectname = poolname
now = str(gf.getTime())

# vm_uuid = "083cb621-76b8-42ba-9728-651cdc795d06"
# network_uuid = sys.argv[8]
# host_uuid =  sys.argv[9]
# if host_uuid == 'null':
#     host_name = gf.compareHost(serverip,serveraccount,serverpwd,projectname)
    
# else:
#     host_uuid = sys.argv[9]
#     host_name = hypervisors.get(host_uuid).hypervisor_hostname
# suspend_num = 3
# host_uuid =  "1" # host id
# sruuid = 1 
# serverip = "140.128.101.205"
# serveraccount = "admin"
# serverpwd = "1j6el4nj4su3"
# poolname = '0'
# operator ="DK"
# guid = "123"
# projectname = admin

glance = client_setting.glance(serverip,serveraccount,serverpwd,projectname)
nova = client_setting.nova(serverip,serveraccount,serverpwd,projectname)
# nova = client_setting.nova()
flavors = nova.flavors
servers = nova.servers
hypervisors = nova.hypervisors
images = nova.images
il = images.list()
vmname = servers.get(vm_uuid).name
Pvm = now+vmname+"_prepareVM"

def create_image():
    servers.create_image(servers.get(vm_uuid),vm_uuid)

    
def scan_vmsnapshot():
    def checkStatus():
        while True:
            time.sleep(1)
            for item in glance.images.list():
                if item.status == "active":
                    return False
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
    twrv = ThreadWithReturnValue(target=checkStatus)
    twrv.start()
    twrv.join()
    for item in il:
        if 'image_type' in item.metadata:
            item_array = {'VM_UUID':item.metadata['instance_uuid'],'SnapShot_UUID':item.id,'SnapShot_Name':item.name,'SnapShot_Date':item.created}
            output += str(item_array)+"\n"
    return output



if __name__ == '__main__':
    create_image()
    f = open(guid+'.txt', 'a')
    f.write(scan_vmsnapshot())
    f.close()
   