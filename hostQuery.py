# -*- coding: utf-8 -*-
from novaclient import client

nova = client.Client(2,"admin","hpc123","admin","http://140.128.101.69:5000/v2.0")
#nova = client.Client(2, "admin", "1j6el4nj4su3", "admin", "http://140.128.101.205:5000/v2.0")
# flavor = nova.flavors.list()
# print(flavor)
hosts = nova.hosts.list_all()

print(hosts[0].host_name)
