# -*- coding: utf-8 -*-
from novaclient import client
import demjson
nova = client.Client(2,"admin","1j6el4nj4su3","admin","http://140.128.101.205:5000/v2.0")




def get_network_ip(vm_net):
    #比對VM的network的label，取得Address
   print vm_net
   nl = networks.list()
   for i in nl:
        for j in vm_net[i.label]:
            return j

#servers define
servers = nova.servers
servers_dict = []

#flavors define
flavors = nova.flavors
networks = nova.networks

#逐個處理每個VM的VALUE
for item in servers.list():
    print(' ')
    VM_UUID = item.id
    VM_Name = item.name
    # 
    flavor_id = item.flavor['id']
    VM_CPUNum = flavors.get(flavor_id).vcpus
    VM_MemoryMB = flavors.get(flavor_id).ram
    
    print item.networks
    VM_IP = get_network_ip(item.networks)
    VM_Status = item.status
    Host_UUID = item.hostId
    
    
    item_array={'VM_UUID':item.id,'VM_Name':item.name,'VM_CPUNum':VM_CPUNum,'VM_MemoryMB':VM_MemoryMB,
    'VM_IP':VM_IP,'VM_Status':VM_Status,'Host_UUID':Host_UUID}
    servers_dict.append(item_array)

json =  demjson.encode(servers_dict)
print(json)







