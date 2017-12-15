# -*- coding: utf-8 -*-
import client_setting
import demjson
import sys
import io
import json 
import time

# #所需參數參數
ServerIp = '140.128.101.205'
ServerAccount = 'admin'
ServerPwd = '1j6el4nj4su3'
PoolName = '0'
Operator = '0'
Guid = 'test'
ProjectName= 'admin'


cinder = client_setting.cinder(ServerIp,ServerAccount,ServerPwd,ProjectName)
# print dir(cinder.scheduler)
volume_pool = cinder.pools.list(detailed=True)
for items in volume_pool:
    print items._info
        # Share_SRUUID = 0
        # Share_SRName = items._info['name']
        # Share_SRTotalSize= items._info['capabilities']['total_capacity_gb']
        # Share_SRFreeSize= items._info['capabilities']['free_capacity_gb']

        # item_array = {"Share_SRUUID":Share_SRUUID,"Share_SRName":Share_SRName,"Share_SRTotalSize":Share_SRTotalSize,"Share_SRFreeSize":Share_SRFreeSize}
        # output += str(item_array)+"\n"