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
nova = client_setting.nova(ServerIp,ServerAccount,ServerPwd,ProjectName)
servers = nova.servers
rlist = neutron.list_routers()
net = neutron.list_networks()
sl = servers.list()

# servers = nova.servers

# sl = servers.list()

scan_list=[]

# for item in rlist['routers']:
# 	scan_list.append({'key':item['name'],'category':'Connector'})

# id_array =[]
#逐個處理每個VM的VALUE
for item in net['networks']:
	scan_list.append({'key':item['name'],'id':item['id'],'category':'Generator'})

for item in sl:
    scan_list.append({'key':item.name,'id':item.id,'category':'Consumer'})
    # id_array.append(item.id)
result = json.dumps(scan_list)
print result