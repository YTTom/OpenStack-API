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

nova = client_setting.nova(ServerIp,ServerAccount,ServerPwd,ProjectName)


servers = nova.servers

sl = servers.list()


vm_array =[]
# id_array =[]
#逐個處理每個VM的VALUE
for item in sl:
    vm_array.append({'key':item.name,'id':item.id,'category':'Consumer'})
    # id_array.append(item.id)
vm_list = json.dumps(vm_array)
print vm_list