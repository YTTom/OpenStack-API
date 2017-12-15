
from novaclient import client
import client_setting
import sys
import io

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
servers = nova.servers




def DelprepareVM():
	VMlist = VM_UUID.split(',')
	# print VMlist
	for vm in VMlist:
		# print servers.get(vm)
		servers.delete(servers.get(vm))
	return 1


DelprepareVM()


