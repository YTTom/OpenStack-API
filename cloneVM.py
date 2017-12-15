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
#python cloneVM.py clonevm abdb657d-f775-4928-9ebe-44cf8bb2f618 45c8adbf-5367-4064-a1b5-2f083c9ac0c7 null 0 1 140.128.101.205 admin 1j6el4nj4su3 admin 0 0 


argv = sys.argv[1]
sourcevm_uuid = sys.argv[2]
network_uuid = sys.argv[3]


sruuid = sys.argv[5]
cmdnum = sys.argv[6]
serverip = sys.argv[7]
serveraccount = sys.argv[8]
serverpwd = sys.argv[9]
poolname = sys.argv[10]
operator =sys.argv[11]
guid = sys.argv[12]
projectname = poolname
now = str(gf.getTime())
host_uuid =  sys.argv[4]
if host_uuid == 'null':
    host_name = gf.compareHost(serverip,serveraccount,serverpwd,projectname)
    
else:
    host_uuid = sys.argv[4]
    host_name = hypervisors.get(host_uuid).hypervisor_hostname


# vm_uuid = "083cb621-76b8-42ba-9728-651cdc795d06"

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
cinder = client_setting.cinder(serverip,serveraccount,serverpwd,projectname)
neutron = client_setting.neutron(serverip,serveraccount,serverpwd,projectname)
nova = client_setting.nova(serverip,serveraccount,serverpwd,projectname)
# nova = client_setting.nova()
flavors = nova.flavors
servers = nova.servers
hypervisors = nova.hypervisors
images = nova.images
vmname = servers.get(sourcevm_uuid).name
Cvm = now+vmname+"_CloneVM"
sl = servers.list()
# snapshot
tmpImage = servers.create_image(servers.get(sourcevm_uuid),sourcevm_uuid)

#create vm use snapshot
flavor_id = servers.get(sourcevm_uuid).flavor['id']
cpu_num = flavors.get(flavor_id).vcpus
memory_mb = flavors.get(flavor_id).ram
vmdisk = flavors.get(flavor_id).disk


def cloneVM(sourcevm_uuid,host_uuid,sruuid,serverip,serveraccount,serverpwd,poolname,operator,guid):
    vm = servers.get(sourcevm_uuid)
    volume_id = vm._info['os-extended-volumes:volumes_attached'][0]['id']
    volume = cinder.volumes.find(id = volume_id)
    volume.reset_state('available')
    volume_name = str(gf.getTime())+volume_id
    snapshot = cinder.volume_snapshots.create(volume_id,name=volume_name)
    while cinder.volume_snapshots.find(id=snapshot.id).status == 'creating':
        time.sleep(5)
    new_volume = cinder.volumes.create(snapshot.size, consistencygroup_id=None,
                   group_id=None, snapshot_id=snapshot.id,
                   source_volid=None, name=volume_name, description=None)
    while cinder.volumes.find(id=new_volume.id).status == 'creating':
        time.sleep(5)
    #status -> in-use
    volume.reset_state('in-use')
    vol = cinder.volumes.find(id=new_volume.id)
    block_dev_mapping = {'vda':vol}
    server_name = Cvm

    sg_list = []
    for item in vm.security_groups:
      sg_list.append(item['id'])
      
    keypair_name = vm.key_name
    body_value = {
                    "port": {
                            "admin_state_up": True,
                            "name": "port",
                            "network_id": network_uuid,
                                                    "fixed_ips":[
                                    {
                                    "subnet_id": '9950c209-2c27-43c8-9e10-2b331ca9d225'
                                    }
                                    ],
                            "security_groups": sg_list,

                          }
                     }
    #nics
    port = neutron.create_port(body=body_value)
    nics = [{'port-id': port['port']['id']}]
    # #keypair find

    server = nova.servers.create(name = server_name, image = None, block_device_mapping = block_dev_mapping, flavor = flavor.id, nics = nics, key_name = keypair_name,availability_zone = host_name,)

    # flavors.delete(tmpF) #創立完VM後刪除
    # flavors.delete(tmpImage) #創立完VM後刪除    
    #f = open('C://eDC/Cmd/'+guid+'.txt', 'a')
cloneVM(sourcevm_uuid,host_uuid,sruuid,serverip,serveraccount,serverpwd,poolname,operator,guid)

# def scan_vm():
#     def print_time( threadName, delay):
#         while True:
#             time.sleep(delay)
#             if servers.get(threadName).status == "ACTIVE":
#                 return servers.get(threadName).status
#                 break
            
        
#     def foo(vmid):
#         while True:
#             time.sleep(1)
#             if servers.get(vmid).status == "ACTIVE":
#                 return servers.get(vmid).status
#                 break
        

#     class ThreadWithReturnValue(Thread):
#         def __init__(self, group=None, target=None, name=None,
#                  args=(), kwargs={}, Verbose=None):
#             Thread.__init__(self, group, target, name, args, kwargs, Verbose)
#             self._return = None
#         def run(self):
#             if self._Thread__target is not None:
#                 self._return = self._Thread__target(*self._Thread__args,
#                                                 **self._Thread__kwargs)
#         def join(self):
#             Thread.join(self)
#             return self._return    
  

#     # #mkdir
#     # isExists=os.path.exists(vm_uuid)
#     # if not isExists:
#     #     os.mkdir(vm_uuid)
#     # #open file
#     # f = open(vm_uuid+'/preparevm.txt', 'a')

    
#     sl = servers.list()
#     output = ""
#     for item in sl:
#     #逐個處理每個VM的VALUE
#         pname = Cvm

#         if item.name == pname:
            
#             # f.write(item.name+"\n")
#             VM_UUID = item.id
#             VM_Name = item.name
#             flavor_id = item.flavor['id']
#             VM_CPUNum = flavors.get(flavor_id).vcpus
#             VM_MemoryMB = flavors.get(flavor_id).ram
#             VM_Status = item.status
#             # pool = ThreadPool(processes=1)
#             # async_result = pool.apply_async(print_time, (VM_UUID, 2)) # tuple of args for foo
#             # VM_Status = async_result.get()  # get the return value from your function.
            
#             twrv = ThreadWithReturnValue(target=foo, args=(VM_UUID,))
#             twrv.start()
#             twrv.join()
#             Host_UUID = item.hostId 
            
#             ip_array=[]
            
#             for n in item.networks: #取得network name
#                 for ip in item.networks[n]: #用network name 去取得IP
#                     ip_array.append(ip)
#             VM_IP=ip_array
#         #
#     #
#             item_array={"SourceVM_UUID":sourcevm_uuid ,"VM_UUID":VM_UUID ,"VM_Name":VM_Name ,"VM_CPUNum":VM_CPUNum ,
#             "VM_MemoryMB":VM_MemoryMB ,"VM_IP":VM_IP ,"VM_Status":VM_Status ,"Host_UUID":Host_UUID,"SRUUID":Host_UUID,
#             "VM_OSType":"none"}
#                 # item_array={"SourceVM_UUID":vm_uuid}
#             output += str(item_array)+"\n"
#         # item.suspend()
        
#     return output

# def scan_vmdisk():
#     output = ""
#     for item in sl:
#         id = item.flavor['id']
#         item_array = {'VM_UUID':item.id,"VMDisk_UUID":" ","VMDisk_Name":" ","SRUUID":" ",'VMDisk_SizeGB':flavors.get(id).disk,"VMDisk_device":"0"}
#         output += str(item_array)+"\n"
#     return output


# def scan_vmnetwork():
#     output = ""

#     for item in sl:
#         VM_UUID = item.id
#         slist = servers.get(VM_UUID)
#         networks = slist.interface_list()
#         subnets = neutron.list_subnets()
#         Vif_UUID = 0
#         vif_device = 0
#         vif_MAC = ""
#         vif_IP = ""
#         for n in item.addresses:
#             vif_MAC = item.addresses[n][0]['OS-EXT-IPS-MAC:mac_addr']
#             vif_IP = item.addresses[n][0]['addr']
#         for item in subnets['subnets']:
#             Network_UUID = item['network_id']
#         item_array = {'VM_UUID':VM_UUID,'Vif_UUID':Vif_UUID,'vif_device':vif_device,'vif_IP':vif_IP,'vif_MAC':vif_MAC,"Network_UUID":Network_UUID}
#         output += str(item_array)+"\n"
#     return output
# def delete():
#     try:
#         images.delete(images.get(tmpImage))
#     except:
#         delete()



if __name__ == '__main__':
    cloneVM(sourcevm_uuid,host_uuid,sruuid,serverip,serveraccount,serverpwd,poolname,operator,guid)
#     f = open(guid+'.txt', 'a')

#     f.write('[vm]\n')
#     f.write(scan_vm())
#     f.write('\n')
#     f.write('[vmdisk]\n')
#     f.write(scan_vmdisk())
#     f.write('\n')
#     f.write('[vmnetwork]\n')
#     f.write(scan_vmnetwork())
#     f.write('\n')
#     f.write('[END]')
#     f.close()
#     delete()
