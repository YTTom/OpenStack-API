# -*- coding: utf-8 -*-
import client_setting
import sys
import io
import json 

ServerIp = '140.128.101.205'
ServerAccount = 'admin'
ServerPwd = '1j6el4nj4su3'
PoolName = 'admin'
ProjectName= PoolName

neutron = client_setting.neutron(ServerIp,ServerAccount,ServerPwd,ProjectName)
nova = client_setting.nova(ServerIp,ServerAccount,ServerPwd,ProjectName)
servers = nova.servers
rlist = neutron.list_routers()
net = neutron.list_networks()
sl = servers.list()

input_value = json.loads(sys.argv[1])
# input_value = [{"to":"demo-net","from":"as881028"},{"to":"demo-net","from":"a"}]

# input_value = json.dumps(argv1)
# input_value = [{"to":"demo-router", "from":"ext-net"},{"to":"demo-net", "from":"rrrr"},{"to":"demo-net", "from":"333"},{"from":"ext-net", "to":"Bar"},{"from":"333", "to":"Bar"}]
# print input_value
input_len = len(input_value)
# input_len2 = len(json.load(input_value))
# print input_len
# print input_value

argv_array=[]
con_array=[]
def choose_action():
	for item in sl:
		for items in item.networks:
			con_array.append({"from":item.name,"to":items})
	# result = json.dumps(con_array)
	# print len(con_array)
	if len(con_array)<input_len:
		add_link()
	else:
		dif = [l for l in con_array if not l in input_value]
		del_link(dif)

# choose_action()

def add_link():
	for item in input_value:
		if item['to'] == "Bar":
			argv_array.append(item['from'])
	net_id = neutron.list_networks(name=argv_array[0])['networks'][0]['id']
	vm_uuid = servers.find(name=argv_array[1]).id
	body_value = {
            "port": {
                    "admin_state_up": True,
                    "device_id": vm_uuid,
                    "name": "port1",
                    "network_id": net_id
                  }
             }
	neutron.create_port(body=body_value)
	print 'ok'
def del_link(dif):
	vm = servers.find(name=dif[0]['from'])
	networks = vm.interface_list()
	port_id = networks[0].port_id
	vm.interface_detach(port_id) #卸載VM網路
	print 'ok'

if __name__ == '__main__':
	choose_action()

