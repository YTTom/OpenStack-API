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
rlist = neutron.list_routers()
nova = client_setting.nova(ServerIp,ServerAccount,ServerPwd,ProjectName)

routers=[]
for item in rlist['routers']:
	routers.append({'key':item['name'],'category':'Connector'})
	r_list = json.dumps(routers)
print r_list

# id_array =[]
#逐個處理每個VM的VALUE
# for item in net['networks']:
# 	print item
# 	vm_array.append({'key':item['id'],'id':item['name'],'category':'Generator'})
# #     vm_array.append({'key':item.name,'id':item.id,'category':'Consumer'})
# #     # id_array.append(item.id)
# vm_list = json.dumps(vm_array)
# print vm_list