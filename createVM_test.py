# -*- coding: utf-8 -*-
from novaclient import client
import client_setting
import globalFunction as gf
# import autoScan 
import time
import sys
import io

# python createVM_test.py createvm yt admin fbce8a2b-02fb-47b8-9d2f-9ddeda2ed75d 20ef3d07-ce9d-4156-b577-09b91b2d4e86 45c8adbf-5367-4064-a1b5-2f083c9ac0c7 9950c209-2c27-43c8-9e10-2b331ca9d225 756b9399-eae3-4c7a-a23b-f3761be8e799,950831aa-0e71-40c3-96a0-7cd5e86f69d3 JoeTestKeyPair 1 2 null 140.128.101.205 admin 1j6el4nj4su3 0 0
argv = sys.argv[1]
server_name = sys.argv[2]
pool_name = sys.argv[3]
template_uuid = sys.argv[4]
flavors_uuid = sys.argv[5]
network_id = sys.argv[6]
subnet_id = sys.argv[7]
keypair_id = sys.argv[8]
sg_id = sys.argv[9]
sruuid = sys.argv[10]

host_uuid =  sys.argv[11] # host id

serverip = sys.argv[12]
serveraccount = sys.argv[13]
serverpwd = sys.argv[14]
operator = sys.argv[15]
guid = sys.argv[16]



cinder = client_setting.cinder(serverip,serveraccount,serverpwd,pool_name)
nova = client_setting.nova(serverip,serveraccount,serverpwd,pool_name)
neutron = client_setting.neutron(serverip,serveraccount,serverpwd,pool_name)
now = gf.getTime()

flavors = nova.flavors
servers = nova.servers
hypervisors = nova.hypervisors

if host_uuid == 'null':
  host_name = gf.compareHost(serverip,serveraccount,serverpwd,pool_name)
  
else:
  # host_uuid = sys.argv[11]
  host_name = hypervisors.get(host_uuid).hypervisor_hostname

# server_name = 'nova-vol-test1'
# template_uuid = "fbce8a2b-02fb-47b8-9d2f-9ddeda2ed75d"
# flavors_uuid ="20ef3d07-ce9d-4156-b577-09b91b2d4e86"
# network_id = '45c8adbf-5367-4064-a1b5-2f083c9ac0c7'
# subnet_id  = '9950c209-2c27-43c8-9e10-2b331ca9d225'
# keypair_id = 'JoeTestKeyPair'



### +++++++++++++++ ###

#image find
image = nova.images.get(template_uuid)

#flavor find
flavor = nova.flavors.get(flavors_uuid)
disk_size = flavor.disk

# volume create
vol1 = cinder.volumes.create(size=disk_size,name='volumes_'+server_name,imageRef=image.id)
cinder.volumes.set_bootable(vol1,True)

while cinder.volumes.find(id=vol1.id).status != 'available':
	time.sleep(5)

block_dev_mapping = {'vda':vol1.id}

# #security group find


sg = sg_id.split(',')
sg_list = []
for item in sg:
    sg_list.append(item)


# # #port create
body_value = {
                "port": {
                        "admin_state_up": True,
                        "name": "port",
                        "network_id": network_id,
                        "fixed_ips":[
          				 			{
               						"subnet_id": subnet_id
            						}
      								],
      					"security_groups": sg_list,

                      }
                 }
#nics
port = neutron.create_port(body=body_value)
nics = [{'port-id': port['port']['id']}]


 

# #keypair find
key_pair = nova.keypairs.get(keypair_id)

#
server = nova.servers.create(name = server_name, image = None, block_device_mapping = block_dev_mapping, flavor = flavor.id, nics = nics, key_name = key_pair.name,availability_zone = 'compute02',)
# Poll at 5 second intervals, until the status is no longer 'BUILD'
status = server.status
# print status
while nova.servers.get(server.id).status != 'ACTIVE':
# for i in range(0,5):
	time.sleep(5)
	vm_new = nova.servers.get(server.id)
	status = vm_new.status
#
output= ""
vm = servers.get(server.id)
VM_UUID = vm.id
flavor_id = vm.flavor['id']
VM_CPUNum = flavors.get(flavor_id).vcpus
VM_MemoryMB = flavors.get(flavor_id).ram
VM_IP = ""
ip_array=[]

for n in vm.networks: #取得network name
	for ip in vm.networks[n]: #用network name 去取得IP
		ip_array.append(ip)
VM_IP=ip_array

VM_Status = vm._info['OS-EXT-STS:power_state']
Host_UUID = vm._info['OS-EXT-SRV-ATTR:host'] 
volume_id =  vm._info['os-extended-volumes:volumes_attached'][0]['id']
volume = cinder.volumes.get(volume_id)
vol_host = volume.__getattr__('os-vol-host-attr:host')
SRUUID= vol_host

if 'OStype' in vm._info['metadata']:
	VM_OSType = vm._info['metadata']['OStype']
else:
	VM_OSType = ' '

Template_UUID = vol1.volume_image_metadata['image_id']


KeyPair_uuid = vm._info['key_name']
if not '' in vm._info['flavor']:
	fv_uuid = vm._info['flavor']['id']
else:
	fv_uuid  = ' '

item_array={'VM_UUID':vm.id,'VM_Name':vm.name,'VM_CPUNum':VM_CPUNum,'VM_MemoryMB':VM_MemoryMB,
'VM_IP':VM_IP,'VM_Status':VM_Status,'Host_UUID':Host_UUID,"SRUUID":SRUUID,"VM_OSType":VM_OSType,"KeyPair_uuid":KeyPair_uuid,"Template_UUID":Template_UUID,"fv_uuid":fv_uuid}
output+=str(item_array)+"\n"


f = open(guid+'.txt', 'a')
f.write('[vm]\n')
f.write(output)
f.close()

#result
  