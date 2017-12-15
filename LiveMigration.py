# -*- coding: utf-8 -*-
import client_setting
import demjson
import sys
import io

argv= sys.argv[1]
VM_UUID = sys.argv[2]
Host_UUID = sys.argv[3]
server_ip = sys.argv[4]
server_account = sys.argv[5]
server_pwd = sys.argv[6]
PoolName = sys.argv[7]
Operator = sys.argv[8]
Guid = sys.argv[9]
project_name = sys.argv[10]


nova = client_setting.nova(server_ip,server_account,server_pwd,project_name)
hypervisors = nova.hypervisors
hl = hypervisors.list()
# VM_UUID = "f7c6157e-71a1-4f40-a5e7-404767f9acd1"

hostname = nova.hypervisors.get(Host_UUID).hypervisor_hostname

try:
	nova.servers.get(VM_UUID).live_migrate(hostname,False,False)
	print '1'
except:
	tp, val, tb = sys.exc_info()
	print sys.stderr, '%s' % (str(val))