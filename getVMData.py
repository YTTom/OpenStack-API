# -*- coding: utf-8 -*-
from novaclient import client
import client_setting
import globalFunction as gf
import sys
import io
import os


argv = sys.argv[1]
vm_uuid = sys.argv[2]
optnum = sys.argv[3]
serverip = sys.argv[4]
serveraccount = sys.argv[5]
serverpwd = sys.argv[6]
poolname = sys.argv[7]
operator =sys.argv[8]
guid = sys.argv[9]
projectname = sys.argv[10]
nova = client_setting.nova(serverip,serveraccount,serverpwd,projectname)
neutron = client_setting.neutron(serverip,serveraccount,serverpwd,projectname)
vm = nova.servers.get(vm_uuid)
servers = nova.servers
sl = servers.list()
networks = vm.interface_list()
subnets = neutron.list_subnets()

# vm ip all
VM_IP=""
ip_array=[]
inip_array=[]
VM_Status=""
VM_IPList=""

def getvmdata():
    for case in gf.switch(optnum):
        if case('0'):
        	scan_vm(0,vm.status,0)
        	break
        if case('1'):
            for item in networks:
            	for fixed_ip  in item.fixed_ips:
            		inip_array.append(fixed_ip['ip_address'])
            scan_vm(str(inip_array),0,0)
            break
        if case('2'):
            for item in networks:
            	for fixed_ip in item.fixed_ips:
            		inip_array.append(fixed_ip['ip_address'])
            for n in vm.networks: #取得network name
                for ip in vm.networks[n]: #用network name 去取得IP
                    ip_array.append(ip)
            s1 = set(inip_array)
            s2 = set(ip_array)
            result = list(s2.difference(s1))
            scan_vm(0,0,str(result))
            break 
	    	#     for ip in vm.networks[n]: #用network name 去取得IP
	    	#         ip_array.append(ip)
	    	# s1 = set(inip_array)
	    	# s2 = set(ip_array)
	    	# result = list(s2.difference(s1))
	    	# scan_vm(0,0,str(result))
        	
        if case('3'):
            for item in networks:
            	for fixed_ip in item.fixed_ips:
            		inip_array.append(fixed_ip['ip_address'])
            for n in vm.networks: #取得network name
                for ip in vm.networks[n]: #用network name 去取得IP
                    ip_array.append(ip)
            s1 = set(inip_array)
            s2 = set(ip_array)
            result = list(s2.difference(s1))
            scan_vm(str(inip_array),0,str(result))
            break

def scan_vm(VM_IP,VM_Status,VM_IPList):
    output = ""
    item_array={'VM_UUID':vm_uuid,'VM_IP':VM_IP,'VM_Status':VM_Status,'VM_IPList':VM_IPList}
    output += str(item_array)+"\n"
    f = open(guid+'.txt', 'a')
    f.write('[vm]\n')
    f.write(output)
    f.write('\n')
    f.write('[END]\n')
    f.close()
    print 1


if __name__ == '__main__':
	getvmdata()
