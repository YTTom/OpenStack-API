# -*- coding: utf-8 -*-
from novaclient import client
import client_setting
import demjson
import sys

#python ChangeVlan.py changevlan a6aee29f-9dd7-45bc-9f4e-74685480e03b 45c8adbf-5367-4064-a1b5-2f083c9ac0c7 0 140.128.101.205 admin 1j6el4nj4su3 admin 0 0
#python ChangeVlan.py changevlan a6aee29f-9dd7-45bc-9f4e-74685480e03b 6459cc90-4623-495c-b877-ddac9a4fcda9 0 140.128.101.205 admin 1j6el4nj4su3 admin 0 0

argument = sys.argv[1] #changevlan
vm_uuid = sys.argv[2]  #虛擬機ID
network_uuid = sys.argv[3] #networkuuid
device_index = int(sys.argv[4])  
serverip = sys.argv[5]		#SERVER IP
serveraccount = sys.argv[6] #帳號
serverpwd = sys.argv[7] 	#密碼
poolname = sys.argv[8]	#projectname
operator = sys.argv[9]	#使用者
guid = sys.argv[10]		#亂數
projectname = poolname	#亂數

# ServerIp = '140.128.101.205'
# ServerAccount = 'admin'
# ServerPwd = '1j6el4nj4su3'
# ProjectName = 'admin'
# port_id = "90ba7ef4-c2cd-49af-8266-cf90e6903e1c"
# net_id =  "c7a28c8d-f7de-4f65-99c9-bbefbea292b9"
# fixed_ip = "192.168.0.106"
	

nova = client_setting.nova(serverip,serveraccount,serverpwd,projectname)
neutron = client_setting.neutron(serverip,serveraccount,serverpwd,projectname)
servers = nova.servers
slist = servers.get(vm_uuid)
sl = servers.list()

# network = nova.networks
# nlist = network.list()
# print dir(nlist[0])
# print nlist[0].bridge

def interface_List():
	output = ""
	networks = slist.interface_list()
	subnets = neutron.list_subnets()
	for item in sl:
		VM_UUID = item.id
		Vif_UUID = 0
        vif_device = 0
        vif_MAC = ""
        vif_IP = ""
        for item in subnets['subnets']:
        	# print item
	    	Network_UUID = item['network_id']
	    	item_array={"VM_UUID":VM_UUID,"Vif_UUID":Vif_UUID ,"vif_device":vif_device,"vif_IP":vif_IP,"vif_MAC": vif_MAC ,"Network_UUID":Network_UUID}
	        output += str(item_array) +"\n"

	# print subnets['subnets'][1]
	# print subnets
	# print '        id:'+subnets['subnets'][1]['id']
	# print 'network_id:'+subnets['subnets'][1]['network_id']       
	
	return output


def interface_Attach():
	networks = slist.interface_list()
	subnets = neutron.list_subnets()
	body_value = {
                "port": {
                        "admin_state_up": True,
                        "device_id": vm_uuid,
                        "name": "port1",
                        "network_id": network_uuid
                      }
                 }
	response = neutron.create_port(body=body_value)
	

def interface_Detach():
	
	networks = slist.interface_list()
	port_id = networks[device_index].port_id
	slist.interface_detach(port_id) #卸載VM網路
	



if __name__ == '__main__':		
	interface_Detach()
	interface_Attach()
	f = open(guid+'.txt', 'a')
	f.write('[vmnetwork]\n')
	f.write(interface_List())
	f.write('[END]\n')
	f.close()
	# interface_List()




	
	

	
	

