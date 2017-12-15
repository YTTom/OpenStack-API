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

argv= sys.argv[1]
vm_uuid = sys.argv[2]
accountStr= sys.argv[3]
pwdStr= sys.argv[4]
serverip = sys.argv[5]
serveraccount = sys.argv[6]
serverpwd = sys.argv[7]
poolname = sys.argv[8]
operator =sys.argv[9]
guid = sys.argv[10]
projectname = sys.argv[11]
now = str(gf.getTime())

# vm_uuid = "083cb621-76b8-42ba-9728-651cdc795d06"
# network_uuid = sys.argv[9]
# host_uuid =  sys.argv[10]
# if host_uuid == 'null':
#     host_name = gf.compareHost(serverip,serveraccount,serverpwd,projectname)
    
# else:
#     host_uuid = sys.argv[10]
#     host_name = hypervisors.get(host_uuid).hypervisor_hostname
# suspend_num = 3
# host_uuid =  "1" # host id
# sruuid = 1 
# serverip = "140.128.101.205"
# serveraccount = "admin"
# serverpwd = "1j6el4nj4su3"
# poolname = '0'
# operator ="DK"
# guid = "thisav"
# projectname = admin

glance = client_setting._glance()
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
    flavor_id = servers.get(vm_uuid).flavor['id']
    VM_CPUNum = flavors.get(flavor_id).vcpus
    VM_MemoryMB = flavors.get(flavor_id).ram
    VM_Disk = flavors.get(flavor_id).disk
       
    for item in il:
        if 'image_type' in item.metadata:
            item_array = {'Template_UUID':item.id,'Template_Name':item.name,'Template_OSType':"0",'Template_CPUNum':VM_CPUNum,'Template_MemoryMB':VM_MemoryMB,'Template_DiskGB':VM_Disk}
            output += str(item_array)+"\n"
    return output



if __name__ == '__main__':
    create_image()
    f = open(guid+'.txt', 'a')
    f.write('[template]')
    f.write(scan_vmsnapshot())
    f.write('\n')
    f.write('[End]')
    f.write('\n')
    f.close()
   