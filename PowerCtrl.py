# -*- coding: utf-8 -*-
import client_setting
import globalFunction as gf
import sys
import io



VM_UUID = sys.argv[1]
ctrlMode = sys.argv[2]
host_uuid =  sys.argv[3] # host id
serverip = sys.argv[4]
serveraccount = sys.argv[5]
serverpwd = sys.argv[6]
pool_name = sys.argv[7]
operator =sys.argv[8]
guid = sys.argv[9]
ProjectName= sys.argv[10]

# VM_UUID = "b50931a2-03de-423a-9a54-981ba997a63f"
# ctrlMode = "start"
# host_uuid =  "0" # host id
# serverip = "140.128.101.205"
# serveraccount = "admin"
# serverpwd = "1j6el4nj4su3"
# pool_name = '0'
# operator ="DK"
# guid = "1234567"

nova = client_setting.nova(serverip,serveraccount,serverpwd,ProjectName)
flavors = nova.flavors
servers = nova.servers
hypervisors = nova.hypervisors
sl = servers.list()


def PowerCtrl(attr,VM_UUID,ctrlMode,Host_UUID,ServerIP,ServerAccount,ServerPwd,PoolName,Operator,guid):
      
    vm = servers.get(VM_UUID)
    # mode = {'start':'start','shutdown':'shutdown','suspend':'suspend','forceshutdown':'shutdown','reboot':'reboot','resume':'resume'}
    
    v = ctrlMode
    for case in gf.switch(ctrlMode):
        if case('shutdown'):
            vm.stop()
            break
        if case('start'):
            vm.start()
            break
        if case('suspend'):
            vm.pause()
            break
        if case('forceshutdown'):
            vm.forceshutdown()
            break
        if case('reboot'): # default, could also just omit condition or 'if True'
            vm.reboot()
            break
        if case('resume'):
        	vm. unpause()
        	break

    return 1


def scan_vm():
    #servers define
   
    output = ""
    #逐個處理每個VM的VALUE
    for item in sl:
        
        VM_UUID = item.id
        VM_Name = item.name
        # 
        flavor_id = item.flavor['id']
        VM_CPUNum = flavors.get(flavor_id).vcpus
        VM_MemoryMB = flavors.get(flavor_id).ram
        VM_IP=""
        #
        ip_array=[]
        for n in item.networks: #取得network name
            for ip in item.networks[n]: #用network name 去取得IP
                ip_array.append(ip)
                
        VM_IP=ip_array
        #
        VM_Status = item.status
        Host_UUID = item.hostId
       
        item_array={'VM_UUID':item.id,'VM_Status':VM_Status,'Host_UUID':Host_UUID}
        output += str(item_array)+"\n"
    return output

PowerCtrl(1,VM_UUID,ctrlMode,host_uuid,serverip,serveraccount,serverpwd,pool_name,operator,guid)
#f = open('C://eDC/Cmd/'+guid+'.txt', 'a')
f = open(guid+'.txt', 'a')
f.write('[vm]\n')
f.write(scan_vm())
f.write('[END]\n')
f.close()