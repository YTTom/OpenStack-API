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
vm_uuid = sys.argv[2]
suspend_num = int(sys.argv[4])
sruuid = sys.argv[5]
serverip = sys.argv[6]
serveraccount = sys.argv[7]
serverpwd = sys.argv[8]
poolname = sys.argv[9]
operator =sys.argv[10]
guid = sys.argv[11]
projectname = sys.argv[12]
now = str(gf.getTime())
host_uuid =  sys.argv[3]
if host_uuid == 'null':
    host_name = gf.compareHost(serverip,serveraccount,serverpwd,projectname)
    
else:
    host_uuid = sys.argv[3]
    host_name = hypervisors.get(host_uuid).hypervisor_hostname


# vm_uuid = "083cb621-76b8-42ba-9728-651cdc795d06"
network_uuid = sys.argv[13]
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


# nova = client_setting.nova(serverip,serveraccount,serverpwd,projectname)
nova = client_setting.nova(serverip,serveraccount,serverpwd,projectname)
glance = client_setting.glance(serverip,serverpwd,serverpwd,projectname)

flavors = nova.flavors
servers = nova.servers
# glance = nova.glances
# images = glance.list()
hypervisors = nova.hypervisors
vmname = servers.get(vm_uuid).name
vm = servers.get(vm_uuid)
Pvm = now+vmname+"_prepareVM"
flavor_id = servers.get(vm_uuid)
# print images



def prepareVM(vm_uuid,suspend_num,host_uuid,sruuid,serverip,serveraccount,serverpwd,poolname,operator,guid):
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

    # snapshot
    tmpImage = servers.create_image(servers.get(vm_uuid),vm_uuid)
    # print tmpImage
    #create vm use snapshot
    flavor_id = servers.get(vm_uuid).flavor['id']
   
    # cpu_num = flavors.get(flavor_id).vcpus
    # memory_mb = flavors.get(flavor_id).ram
    # vmdisk = flavors.get(flavor_id).disk

    
    
    tmpId = gf.createRamdom()
    tmpFlavorName = str(now)+"_flavor"  #補亂數以免同名
    # tmpF = flavors.create(tmpFlavorName,memory_mb,cpu_num,vmdisk,tmpId,0,0) #建立VM前先創立符合需求的flavors
    def create_server():
            servers.create(name = Pvm,
            image = tmpImage,
            flavor = flavor_id,
            nics = [{'net-id':network_uuid}],
            availability_zone = host_name,
            max_count = suspend_num
            )

    def checktask():       
        while True:
            time.sleep(10)      
            # print glance.images.get(tmpImage).status
            if  glance.images.get(tmpImage).status == "active":
                create_server()
                break

    twrv = ThreadWithReturnValue(target=checktask, args=(),)
    twrv.start()
    twrv.join()
    
  
    
        # #flavors.delete(tmpF) #創立完VM後刪除
        
    #f = open('C://eDC/Cmd/'+guid+'.txt', 'a')
    

def scan_vm():
    def checkStatus(vmid):
        while True:
            time.sleep(1)
           
            if servers.get(vmid).status == "ACTIVE":
                return servers.get(vmid).status
                break
    def checkHost(vmid):
        while True:
            time.sleep(1)
            if servers.get(vmid).__getattr__('OS-EXT-SRV-ATTR:host') != "":
                return servers.get(vmid).__getattr__('OS-EXT-SRV-ATTR:host')
                break

    def checkIP(vmid):
        time.sleep(5)
        ip_array=[]

        for n in servers.get(vmid).networks: #取得network name
            for ip in servers.get(vmid).networks[n]: #用network name 去取得IP
                ip_array.append(ip)
        VM_IP=ip_array

        return VM_IP
        

    def getHypervisors(hostname):
        for item in hypervisors.list():
            if item.hypervisor_hostname == hostname:
                return item.id


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
  

    #mkdir
    isExists=os.path.exists(vm_uuid)
    if not isExists:
        os.mkdir(vm_uuid)
    #open file
    f = open(vm_uuid+'/preparevm.txt', 'a')

    sl = servers.list()
    output = ""
    
    for i in range(suspend_num):
        for item in sl:
        #逐個處理每個VM的VALUE
            j=i+1
            if suspend_num >1:
                pname = Pvm+'-'+str(j) 
            else:
                pname = Pvm

            if item.name == pname:
                
                f.write(item.name+"\n")
                
                VM_UUID = item.id
                VM_Name = item.name
                flavor_id = item.flavor['id']
                VM_CPUNum = flavors.get(flavor_id).vcpus
                VM_MemoryMB = flavors.get(flavor_id).ram
                
                # pool = ThreadPool(processes=1)
                # async_result = pool.apply_async(print_time, (VM_UUID, 2)) # tuple of args for foo
                # VM_Status = async_result.get()  # get the return value from your function.
                
                twrv = ThreadWithReturnValue(target=checkStatus, args=(VM_UUID,))
                twrv.start()
                VM_Status = twrv.join()

                # Host_UUID = item.hostId 
                twrv = ThreadWithReturnValue(target=checkHost, args=(VM_UUID,))
                twrv.start()
                Host_UUID = getHypervisors(twrv.join())
                # VM_Status = item.status

                twrv = ThreadWithReturnValue(target=checkIP, args=(VM_UUID,))
                twrv.start()
                VM_IP = twrv.join()
               
                
               
            #
                item_array={"SourceVM_UUID":vm_uuid ,"VM_UUID":VM_UUID ,"VM_Name":item.name ,"VM_CPUNum":VM_CPUNum ,
                "VM_MemoryMB":VM_MemoryMB ,"VM_IP":VM_IP ,"VM_Status":VM_Status ,"Host_UUID":Host_UUID,"SRUUID":Host_UUID,
                "VM_OSType":"none"}
                    # item_array={"SourceVM_UUID":vm_uuid}
                output += str(item_array)+"\n"
                item.pause()
    
    f.close()
   
        
    return output



if __name__ == '__main__':

    prepareVM(vm_uuid,suspend_num,host_uuid,sruuid,serverip,serveraccount,serverpwd,poolname,operator,guid)
    f = open(guid+'.txt', 'a')
    f.write(scan_vm())
    f.close()
    print 1