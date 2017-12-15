# -*- coding: utf-8 -*-
from novaclient import client
import client_setting
import globalFunction as gf
import sys
import io
import os

argv = sys.argv[1] #delvm
VM_UUID=sys.argv[2]
optnum= int(sys.argv[3])
ServerIP=sys.argv[4]
ServerAccount=sys.argv[5]
ServerPwd=sys.argv[6]
PoolName=sys.argv[7]
Operator=sys.argv[8]
guid=sys.argv[9]
projectname=sys.argv[10]


nova = client_setting.nova(ServerIP,ServerAccount,ServerPwd,projectname)
flavors = nova.flavors
servers = nova.servers
hypervisors = nova.hypervisors


def horizontalReduce():
	for case in gf.switch(optnum):
	    if case(1):
	    	print 1
	        servers.delete(servers.get(VM_UUID))
	        break
	    if case(2):
	    	print 2
	        servers.get(VM_UUID).suspend()
	        break
	return 1

  




horizontalReduce()


