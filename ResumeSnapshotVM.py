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
snapshot_uuid =  sys.argv[3]
serverip = sys.argv[4]
serveraccount = sys.argv[5]
serverpwd = sys.argv[6]
poolname = sys.argv[7]
operator =sys.argv[8]
guid = sys.argv[9]
projectname = sys.argv[10]



# nova = client_setting.nova(serverip,serveraccount,serverpwd,projectname)
nova = client_setting.nova(serverip,serveraccount,serverpwd,projectname)
flavors = nova.flavors
servers = nova.servers
hypervisors = nova.hypervisors
vmname = servers.get(vm_uuid).name
flavor_id = servers.get(vm_uuid)

def resumesnapshotvm(vm_uuid,snapshot_uuid):
	nova.servers.get(vm_uuid).rebuild(snapshot_uuid) #vm-uuid image_id
	print 1


if __name__ == '__main__':
	resumesnapshotvm(vm_uuid,snapshot_uuid)
