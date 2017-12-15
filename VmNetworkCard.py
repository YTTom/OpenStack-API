# -*- coding: utf-8 -*-
from novaclient import client
import client_setting
import demjson
import sys

argument = sys.argv[1] #VmNetworkCard
vm_uuid = sys.argv[2]  #虛擬機ID
ctrlitem = sys.argv[3] #動作(刪或加)
network_uuid = sys.argv[4]  #net_id 刪除可不用
networktype = sys.argv[5]	#網卡類別　刪除可不用
network_device = int(sys.argv[6]) #第幾張網卡 刪除才需要
serverip = sys.argv[7]		#SERVER IP
serveraccount = sys.argv[8] #帳號
serverpwd = sys.argv[9] 	#密碼
poolname = sys.argv[10]	#Pool
operator = sys.argv[11]	#使用者
guid = sys.argv[12]		#亂數
projectname = sys.argv[13]		#亂數

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
	port_id = networks[network_device].port_id
	slist.interface_detach(port_id) #卸載VM網路
	


		
if ctrlitem == '1': #加網卡
    interface_Attach()
    f = open('VmNetworkCard.txt', 'a')
    f.write('[vmnetwork]\n')
    f.write(interface_List())
    f.write('[END]\n')
    f.close()
    print 1
elif ctrlitem == '2': #刪網卡

	interface_Detach()

	print 1
	# elif ctrlitem == '3':
	# 	interface_List()
	# 	print 3
else:
	#print dir(slist[0])
	#networks = slist.interface_list()
	subnets = neutron.list_subnets()
	print 'Please type 1 or 2'



	
	

	
	

