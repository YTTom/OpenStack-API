# -*- coding: utf-8 -*-
import client_setting
import sys
import io
import globalFunction as gf


now = gf.getTime()

#輸入參數
ServerIp = sys.argv[1]
ServerAccount = sys.argv[2]
ServerPwd = sys.argv[3]
ProjectName = sys.argv[4]
flavorsName = sys.argv[5]
cpuNum = sys.argv[6]
ram = sys.argv[7]
rootDisk = sys.argv[8]
swapDisk = sys.argv[9]
Operator = sys.argv[10]
Guid = sys.argv[11]

#
nova = client_setting.nova(ServerIp,ServerAccount,ServerPwd,ProjectName)


flavors = nova.flavors
servers = nova.servers
hypervisors = nova.hypervisors

def createFlavors(flavors_name,cpuNum,ram,rootDisk,swapDisk):
	tmpId = gf.createRamdom()
	Flavor = flavors.create(flavors_name,ram,cpuNum,rootDisk,tmpId,0,0) #建立VM前先創立符合需求的flavors
	return 1
    
if __name__ == '__main__':
   createFlavors(flavorsName,cpuNum,ram,rootDisk,swapDisk)





