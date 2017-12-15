# -*- coding: utf-8 -*-
import client_setting
import demjson
import sys
import io
import json 

# python autoScan.py 140.128.101.205 admin 1j6el4nj4su3 admin 0 0

# #所需參數參數
ServerIp = sys.argv[1]
ServerAccount = sys.argv[2]
ServerPwd = sys.argv[3]
PoolName = sys.argv[4]
Operator = sys.argv[5]
Guid = sys.argv[6]
ProjectName= PoolName

nova = client_setting.nova(ServerIp,ServerAccount,ServerPwd,ProjectName)
neutron = client_setting.neutron(ServerIp,ServerAccount,ServerPwd,ProjectName)
glance = client_setting.glance(ServerIp,ServerAccount,ServerPwd,ProjectName)
cinder = client_setting.cinder(ServerIp,ServerAccount,ServerPwd,ProjectName)
# nova = client_setting._nova()
# neutron = client_setting._neutron()
# glance = client_setting._glance()

hypervisors = nova.hypervisors
servers = nova.servers
flavors = nova.flavors
networks = nova.networks
images = nova.images
securitygroup = nova.security_groups
keypairs = nova.keypairs

hl = hypervisors.list()
nl = networks.list()
il = images.list()
sl = servers.list()
fl = flavors.list()
net = neutron.list_networks()
volumes = cinder.volumes.list()
subnets = neutron.list_subnets()



def scan_host():
    hl = nova.hypervisors.list()
    output = ""
    for item in hl:
        Host_UUID =item.id
        Host_Name = item.hypervisor_hostname
        Host_IP =item.host_ip

        j=demjson.decode(item.cpu_info)
        CPU_count=j['topology']['cores']
        CPU_GHZ = 0
        CPU_Socket = j['topology']['sockets']
        MemoryMB=item.memory_mb
        
        #check hosts state
        PowerOn = 0

        if(item.state == 'up'):
            PowerOn = 1
        else:
            PowerOn = 0
        #
        item_array={'Host_UUID':Host_UUID,'Host_Name':Host_Name,'Host_IP':Host_IP,'CPU_Count':CPU_count,'CPU_GHZ':CPU_GHZ,'CPU_Socket':CPU_Socket,
        'MemoryMB':MemoryMB,'PowerOn':PowerOn} 
        output += str(item_array) +"\n"

        #
    
    # json =  demjson.encode(hosts_dict)
    return output

def scan_localstorage():
    output = ""
    for item in hl:
        Host_UUID = item.id
        Local_SRName = item.hypervisor_hostname
        Local_StorageSize = item.local_gb
        Local_StorageFreeSize = item.free_disk_gb
        Local_SRUUID = item.id
        item_array={'Host_UUID':Host_UUID,'Local_SRUUID':Local_SRUUID,'Local_SRName':Local_SRName,'Local_StorageSize':Local_StorageSize,'Local_StorageFreeSize':Local_StorageFreeSize} 
        output += str(item_array) +"\n"
    return output

def scan_network():
    output = ""
    # subnets = neutron.list_subnets()
    # for item in subnets['subnets']:
    #     Network_UUID = item['network_id']
    #     Network_Name = item['name']
    #     Network_VlanID = 0
    #     Network_Ip_Pool = item['allocation_pools']
    for item in net['networks']:
        Network_UUID = item['id']
        Network_Name = item['name']
        Network_VlanID = '0'
        item_array={'Network_UUID':Network_UUID,'Network_Name':Network_Name,'Network_VlanID':Network_VlanID} 
        output += str(item_array) +"\n"
    return output
#openstack image
def scan_template():
    output = ""
    for images in glance.images.list():
        if not 'image_type' in images and not 'block_device_mapping' in images:
            if not 'iso' in images.disk_format:
                if 'OStype' in images :
                    OStype = images.OStype
                    Template_UUID = images.id
                    Template_Name = images.name
                else:
                    OStype = ''
                    Template_UUID = images.id
                    Template_Name = images.name
                # print OStype
                # OStype = images.OStype
                item_array={'Template_UUID':Template_UUID,'Template_Name':Template_Name,'Template_OSType':OStype,'Template_CPUNUM':0,'Template_MemoryMB':0,'Template_DiskGB':0}
                output += str(item_array)+"\n"
    return output

# openstack template 
def scan_Flavors():
    flavors = nova.flavors.list()
    output = ""
    for item in flavors:
        item_array={'fv_uuid':str(item.id),'fv_name':str(item.name),'fv_memory':str(item.ram),'fv_cpu':str(item.vcpus),'fv_disk':str(item.disk)}
        output += str(item_array)+"\n"
    return output


def scan_vm():
    # def getHypervisors(hostname):
    #     for item in hypervisors.list():
    #         if item.hypervisor_hostname == hostname:
    #             return item.id

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
        VM_Status = item._info['OS-EXT-STS:power_state']
        # Host_UUID = getHypervisors(item.__getattr__('OS-EXT-SRV-ATTR:host'))
        if 'OStype' in item._info['metadata']:
            VM_OSType = item._info['metadata']['OStype']
        else:
            VM_OSType = ' '

        KeyPair_uuid = item._info['key_name']
        if not '' in item._info['image']:
            Template_UUID = item._info['image']['id']
        else:
            Template_UUID = ' '
        if not '' in item._info['flavor']:
            fv_uuid = item._info['flavor']['id']
        else:
            fv_uuid  = ' '

        Host_UUID = item._info['OS-EXT-SRV-ATTR:host']
        SRUUID = 0

        item_array={'VM_UUID':item.id,'VM_Name':item.name,'VM_CPUNum':VM_CPUNum,'VM_MemoryMB':VM_MemoryMB,
        'VM_IP':VM_IP,'VM_Status':VM_Status,'Host_UUID':Host_UUID,"SRUUID":SRUUID,"VM_OSType":VM_OSType,"KeyPair_uuid":KeyPair_uuid,"Template_UUID":Template_UUID,"fv_uuid":fv_uuid}
        output += str(item_array)+"\n"
    return output

def Subnet():
    output= ""
# Subnet_uuid = 0
# Subnet_name = 0
    # Subnet_Status = 0
# Network_UUID = 0
# cidr = 0
# Subnet_start= 0
# Subnet_end = 0
    for items in subnets['subnets']:
        # print items
        Subnet_start = items['allocation_pools'][0]['start']
        Subnet_end = items['allocation_pools'][0]['end']
        cidr = items['cidr']
        Subnet_name = items['name']
        Subnet_uuid = items['id']
        Network_UUID = items['network_id']
        item_array={"Subnet_uuid":Subnet_uuid, "Subnet_name":Subnet_name,"Network_UUID":Network_UUID,"cidr":cidr,"Subnet_start":Subnet_start,"Subnet_end":Subnet_end}

        output += str(item_array)+"\n"
    return output
def scan_vmdisk():
    output = ""
    for items in volumes:
        VMDisk_UUID = items.id
        VMDisk_Name = items.name
        vol = cinder.volumes.get(items.id)
        vol_host = vol.__getattr__('os-vol-host-attr:host')
        SRUUID = vol_host
        VMDisk_SizeGB = items.size

        if not items.name:
            VMDisk_Name = items.id    
        else:
            VMDisk_Name = items.name

        if not items.attachments:
            VM_UUID = ' '
            VMDisk_device = ' '
        else:
            VM_UUID = items.attachments[0]['server_id']
            VMDisk_device = items.attachments[0]['device']
        # print VMDisk_device
        # print items._info
        # print dir(items)
        item_array = {"VM_UUID": VM_UUID ,"VMDisk_UUID":VMDisk_UUID,"VMDisk_Name":VMDisk_Name,"SRUUID":SRUUID,"VMDisk_SizeGB":VMDisk_SizeGB,"VMDisk_device":VMDisk_device}
        output += str(item_array)+"\n"
    return output


def sg_id(sg_name):
    sg = neutron.list_security_groups()
    for item in sg['security_groups']:
        if sg_name == item['name']:
            return item['id']



def scan_vmnetwork():
    output = ""
    for item in sl:
        device_array=[]
        vif_uuid_array=[]
        mac_array=[]
        VM_UUID = item.id
        vm = servers.get(VM_UUID)
        # print vm._info
        vif_IP = vm.networks
        # vif_MAC = 0
        # Network_UUID = 0
        Vif_UUID = 0
        all_sg = []
        if 'security_groups'in vm._info :
            for sg in  vm._info['security_groups']:
                sg_uuid = sg_id(sg['name'])
                all_sg.append(sg_uuid)

        else:
            sg_uuid= ''

        networks = vm.interface_list()
        subnets = neutron.list_subnets()
        # print subnets
        for items in networks:
            # print dir(items)
            mac_array.append(items._info['mac_addr'])
            vif_uuid = items.id
            vif_uuid_array.append(vif_uuid)

        Vif_UUID = vif_uuid_array
        vif_MAC = mac_array
        all_ip = []
        all_netid=[]
        all_subnets=[]

        for items in vm.networks:
            all_ip.append(vm.networks[items])
            vm_net = neutron.list_networks(name=items)['networks'][0]  #列出所有network
            all_netid.append(vm_net['id'])
            all_subnets.append(vm_net['subnets'])

            vif_time = vm_net['created_at'] #network建立時間 用來排序vif_device
            
            vif_array=[]
            for item in nl:
                vid = item._info['id']
                vm_net = neutron.list_networks(id=item._info['id'])['networks'][0]  #列出所有network
                t = vm_net['created_at'] #建立時間
                # print vm_net['created_at']
                # print type(vif_array)
                vif_array.append(t)
                # print vif_array
            vif_array.sort()
            for i in range(0,len(vif_array)):
                # print 'input '+vif_time
                # print 'All network '+vif_array[i]
                if vif_time == vif_array[i]:
                    device_array.append(str(i))

            vif_device = device_array
            vif_IP = all_ip
            Network_UUID = all_netid
            Subnet_uuid = all_subnets
            item_array = {"VM_UUID":VM_UUID,"Vif_UUID":Vif_UUID,"vif_device":vif_device ,"vif_IP":vif_IP,"vif_MAC":vif_MAC,"Network_UUID":Network_UUID,"Subnet_uuid":Subnet_uuid,"sg_uuid":all_sg}   
            output += str(item_array)+"\n"
    return output

def set_device(vif_time):
    vif_array=[]
    device_array =[]

    for item in nl:
        vid = item._info['id']
        vm_net = neutron.list_networks(id=item._info['id'])['networks'][0]  #列出所有network
        t = vm_net['created_at'] #建立時間
        # print vm_net['created_at']
        # print type(vif_array)
        vif_array.append(t)
        # print vif_array
    vif_array.sort()
    for i in range(0,len(vif_array)):
        # print 'input '+vif_time
        # print 'All network '+vif_array[i]
        if vif_time == vif_array[i]:

            
            device_array.append(str(i))
    return device_array

def scan_vmsnapshot():
    output = ""
    for item in il:
        if 'image_type' in item.metadata:
            item_array = {'VM_UUID':item.metadata['instance_uuid'],'SnapShot_UUID':item.id,'SnapShot_Name':item.name,'SnapShot_Date':item.created,'minDisk':item.minDisk}
            output += str(item_array)+"\n"
    return output
 
def scan_securitygroup():
    output = ""

    for item in securitygroup.list():
        item_array = {'id':item.id,'name':item.name,'rules':item.rules}
        output += str(item_array)+"\n"
    return output

def scan_keypairs():
    output = ""

    for item in keypairs.list():
        item_array = {"KeyPair_uuid":item.id,"KeyPair_name":item.name,"KeyPair_publickey":item.public_key}
        output += str(item_array)+"\n"
    return output

def Sharestroage():
    output = ""
    volume_pool = cinder.pools.list(detailed=True)
    for items in volume_pool:
        # print items._info
        Share_SRUUID = 0
        Share_SRName = items._info['name']
        Share_SRTotalSize= items._info['capabilities']['total_capacity_gb']
        Share_SRFreeSize= items._info['capabilities']['free_capacity_gb']

        item_array = {"Share_SRUUID":Share_SRUUID,"Share_SRName":Share_SRName,"Share_SRTotalSize":Share_SRTotalSize,"Share_SRFreeSize":Share_SRFreeSize}
        output += str(item_array)+"\n"
    return output
    
f = open('autoscan.txt', 'a') 
f.write('[host]\n')
f.write(scan_host())
f.write('\n')

f.write('[localstorage]\n')
f.write(scan_localstorage()) 
f.write('\n')

f.write('[sharestroage]\n')
f.write(Sharestroage())
f.write('\n')

f.write('[network]\n')
f.write(scan_network())
f.write('\n')

f.write('[template]\n')
f.write(scan_template())
f.write('\n')

f.write('[vm]\n')
f.write(scan_vm())
f.write('\n')

f.write('[vmdisk]\n')
f.write(scan_vmdisk())
f.write('\n')

f.write('[vmnetwork]\n')
f.write(scan_vmnetwork())
f.write('\n')

f.write('[vmsnapshot]\n')
f.write(scan_vmsnapshot())
f.write('\n')

f.write('[flavors]\n')
f.write(scan_Flavors())
f.write('\n')

f.write('[SecurityGroup]\n')
f.write(scan_securitygroup())
f.write('\n')

f.write('[Subnet]\n')
f.write(Subnet())
f.write('\n')

f.write('[keypairs]\n')
f.write(scan_keypairs())
f.write('\n')

f.write('[End]')

f.close()

