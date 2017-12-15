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
vm_uuid = sys.argv[1]
Host_UUID = sys.argv[2]
# suspend_num = int(sys.argv[2])


# sruuid = sys.argv[4]
# serverip = sys.argv[5]
# serveraccount = sys.argv[6]
# serverpwd = sys.argv[7]
# poolname = sys.argv[8]
# operator =sys.argv[9]
# guid = sys.argv[10]
# projectname = sys.argv[11]
# now = str(gf.getTime())
# host_uuid =  sys.argv[3]
# if host_uuid == 'null':
#     host_name = gf.compareHost(serverip,serveraccount,serverpwd,projectname)
    
# else:
#     host_uuid = sys.argv[3]
#     host_name = hypervisors.get(host_uuid).hypervisor_hostname



serverip = "140.128.101.205"
serveraccount = "admin"
serverpwd = "1j6el4nj4su3"

projectname = 'admin'


nova = client_setting.nova(serverip,serveraccount,serverpwd,projectname)
# nova = client_setting.nova()
flavors = nova.flavors
servers = nova.servers
hypervisors = nova.hypervisors
images = nova.images
il = images.list()
# vmname = servers.get(vm_uuid).name
# Pvm = now+vmname+"_prepareVM"

hl = hypervisors.list()
for item in hypervisors.list():
    if item.hypervisor_hostname == Host_UUID:
        print item.id