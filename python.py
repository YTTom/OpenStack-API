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

net = neutron.list_networks()

hl = hypervisors.list()
nl = networks.list()
il = images.list()
sl = servers.list()
fl = flavors.list()
volumes = nova.volumes

vmuuid = '607e2966-45af-4e3b-8bad-0a75ca18da65'
deviceidx = '2'
addGB = 40
# vm = servers.get('2a8edd3f-0b2a-493a-a855-d3fa1d727aec')
vm = servers.get(vmuuid)
print vm.networks
# sg_list = []
# for item in vm.security_groups:
# 	sg_list.append(item['name'])
# print sg_list
# print (dir(vm))
# print vm.security_groups

# # print sl[0].get_spice_console('spice-html5')['console']['url']
# # print sl[0].get_vnc_console('novnc')['console']['url']
# volume_id = 'a0342f29-0a4c-4395-806e-d8eca8fbdc66'
# volume = cinder.volumes.find(id = volume_id)
# # print cinderid
# volume.reset_state('available')
# new_vl = cinder.volume_snapshots.create(volume_id,name='opop')
# vstatus = new_vl.status
# while vstatus != 'available':
# 	time.sleep(5)
# 	new_vl2 = cinder.volume_snapshots.get(new_vl.id)
# 	vstatus = new_vl2.status
# created_volume = cinder.volumes.create(15,snapshot_id=new_vl.id,name='opopopopop') #create volume
# volume_status = created_volume.status
# while volume_status != 'available':
# 	time.sleep(5)
# 	now_volume = cinder.volumes.find(id = created_volume.id)
# 	volume_status = now_volume.status

# network_id = '45c8adbf-5367-4064-a1b5-2f083c9ac0c7'
# subnet_id = '9950c209-2c27-43c8-9e10-2b331ca9d225'
# sg_list = ['14d172c9-ac1c-44be-91b5-9e71df48cc2b']
# server_name = 'useeboy'
# flavors_uuid = 'e2685c3f-6866-4ae9-94a5-b93711ea5b0c'
# flavor = nova.flavors.get(flavors_uuid)
# keypair_id = '123'
# block_dev_mapping = {'vda':created_volume.id}
# body_value = {
#                 "port": {
#                         "admin_state_up": True,
#                         "name": "port",
#                         "network_id": network_id,
#                         "fixed_ips":[
#           				 			{
#                						"subnet_id": subnet_id
#             						}
#       								],
#       					"security_groups": sg_list,

#                       }
#                  }
# #nics
# port = neutron.create_port(body=body_value)
# nics = [{'port-id': port['port']['id']}]

# # #keypair find
# key_pair = nova.keypairs.get(keypair_id)

# #
# server = nova.servers.create(name = server_name, image = None, block_device_mapping = block_dev_mapping, flavor = flavor.id, nics = nics, key_name = key_pair.name,availability_zone = 'compute02',)
# # Poll at 5 second intervals, until the status is no longer 'BUILD'
# # status = server.status	

# # print dir(cinder)
