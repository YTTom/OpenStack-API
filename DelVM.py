# -*- coding: utf-8 -*-
from novaclient import client
import client_setting
import globalFunction as gf
import sys
import io
import os

argv = sys.argv[1] #delvm
VM_UUID=sys.argv[2]
ServerIP=sys.argv[3]
ServerAccount=sys.argv[4]
ServerPwd=sys.argv[5]
PoolName=sys.argv[6]
Operator=sys.argv[7]
guid=sys.argv[8]
projectname=sys.argv[9]


nova = client_setting.nova(ServerIP,ServerAccount,ServerPwd,projectname)
flavors = nova.flavors
servers = nova.servers
hypervisors = nova.hypervisors


def DelVM(argv,VM_UUID,ServerIP,ServerAccount,ServerPwd,PoolName,Operator,guid):
    servers.delete(servers.get(VM_UUID))




DelVM(argv,VM_UUID,ServerIP,ServerAccount,ServerPwd,PoolName,Operator,guid)
print 1

