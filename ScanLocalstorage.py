# -*- coding: utf-8 -*-
from novaclient import client
import demjson
nova = client.Client(2,"admin","1j6el4nj4su3","admin","http://140.128.101.205:5000/v2.0")

hl = nova.hypervisors.list()
hosts_dict=[]
for item in hl:
    Host_UUID = item.id
    Local_SRName = item.hypervisor_hostname
    Local_SRTotalSize = item.local_gb
    Local_SRFreeSize = item.free_disk_gb

    item_array={'Host_UUID':Host_UUID,'Local_SRUUID':0,'Local_SRName':Local_SRName,'Local_SRTotalSize':Local_SRTotalSize,'Local_SRFreeSize':Local_SRFreeSize} 
    hosts_dict.append(item_array)

json =  demjson.encode(hosts_dict)
print(json)

