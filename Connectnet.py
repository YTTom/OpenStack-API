# -*- coding: utf-8 -*-
import client_setting
# import sys
import json 

# python autoScan.py 140.128.101.205 admin 1j6el4nj4su3 admin 0 0

# #所需參數參數
ServerIp = '140.128.101.205'
ServerAccount = 'admin'
ServerPwd = '1j6el4nj4su3'
PoolName = 'admin'
ProjectName= PoolName

neutron = client_setting.neutron(ServerIp,ServerAccount,ServerPwd,ProjectName)
net = neutron.list_networks()
router = neutron.list_routers()
nova = client_setting.nova(ServerIp,ServerAccount,ServerPwd,ProjectName)

# net = neutron.list_router()

servers = nova.servers

sl = servers.list()
# network = neutron.list_networks()

con_array =[]
# id_array =[]
#逐個處理每個VM的VALUE
# print neutron.list_networks(id='e8474a20-12c4-4e3a-aaf7-490e2322f4c2')
# for item in router['routers']:
# 	# print item
# 	router_name = item['name']
# 	gate_network_id = item['external_gateway_info']['network_id']
# 	gate_network_name = neutron.list_networks(id=gate_network_id)['networks'][0]['name']
# 	con_array.append({"from":gate_network_name,"to":router_name})
con_array.append({"from":"ext-net","to":"demo-net"})
for item in sl:
	# print item.networks
	for items in item.networks:
		# print item
		con_array.append({"from":item.name,"to":items})
result = json.dumps(con_array)
print result