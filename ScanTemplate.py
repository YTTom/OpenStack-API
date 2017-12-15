# -*- coding: utf-8 -*-
from novaclient import client
import demjson
nova = client.Client(2,"admin","hpc123","admin","http://140.128.101.69:5000/v2.0")

flavors = nova.flavors.list()
flavors_dict = []

for item in flavors:
    my_array={'Template_UUID':str(item.id),'name':str(item.name),'ram':str(item.ram),'vcpus':str(item.vcpus),'disk':str(item.disk),'swap':str(item.swap),'rxtx_factor':str(item.rxtx_factor)}
    flavors_dict.append(my_array)

json =  demjson.encode(flavors_dict)
print(json)

