# -*- coding: utf-8 -*-
import client_setting
import globalFunction as gf
import sys
import io

#python ResourceModify_new.py resourcemodify 2a97d4cc-e894-4b88-b8f9-d4076a16e383 89210052-36fb-4c9b-a0ac-080b50616a63 0 0 0 0 140.128.101.205 admin 1j6el4nj4su3 1 1 1 admin
argv=sys.argv[1]
vmuuid=sys.argv[2]
# cpu_num=sys.argv[2]
# memory_mb=sys.argv[3]
flavor_uuid = sys.argv[3]
addGB=sys.argv[4]
diskctrl = sys.argv[5]
deviceidx = sys.argv[6]
sruuid =sys.argv[7]
server_ip =  sys.argv[8]
server_account = sys.argv[9]
server_pwd = sys.argv[10]
poolname =sys.argv[11]
operator =sys.argv[12]
guid =sys.argv[13]
project_name=sys.argv[14]

# vmuuid="cf8f5293-050c-41a8-83ac-85e0beec8df6"
# cpu_num=2
# memory_mb=2048
# addGB=3
# diskctrl = 2
# deviceidx = 0
# sruuid =0
# serverip =  "140.128.101.205"
# serveraccount = "admin"
# serverpwd ="1j6el4nj4su3"
# poolname =""
# operator =""
# guid =""
# projectname = "admin"

now = gf.getTime()
nova = client_setting.nova(server_ip,server_account,server_pwd,project_name)
# nova = client_setting.nova(serverip,serveraccount,serverpwd,projectname)
neutron = client_setting.neutron(server_ip,server_account,server_pwd,project_name)
cinder = client_setting.cinder(server_ip,server_account,server_pwd,project_name)
volumes = nova.volumes
servers = nova.servers
flavors = nova.flavors
networks = nova.networks
hypervisors = nova.hypervisors
images = nova.images
ip = nova.floating_ips
hl = hypervisors.list()
nl = networks.list()
il = images.list()
sl = servers.list()
fl = flavors.list()



def ResourceModify():
	# 取得原本VM的flavor資訊
	vm = servers.get(vmuuid)
	rawFlavorId = vm.flavor['id']
	rawFlavor = flavors.get(rawFlavorId)
	
	# #建立一個暫時的flavor 用來改變VM的ram cpu disk
	# #now 為當下的時間戳記
	tmpFlavorName = str(now)+"_flavor" 


	#根據diskCtrl 來決定要對硬碟做的操作
	for case in gf.switch(int(diskctrl)):
		if case(0):
			#不調整硬碟
			#所以用原本的硬碟大小來產生flavors
			tmpF = flavors.get(flavor_uuid)

			#然後用這個flavor去更改指定VM的設定
			try:
				vm.resize(tmpF)
			except:
				print 'resize fail'


			def check_confirm(vm):
				try:
					vm.confirm_resize()
					print '1'
				except:
					check_confirm(vm)
						
			check_confirm(vm)
			
			break

		if case(1):
			#新增硬碟

			#新增雲硬碟
			cinder.volumes.create(size=addGB,name=tmpFlavorName)
			cinderid = cinder.volumes.find(name = tmpFlavorName).id
			tmpF = flavors.get(flavor_uuid)
			
			#resize
			try:
				vm.resize(tmpF)
			except:
				print 'resize fail'

			def create_server_volume(vm,volume):
				try:
					volumes.create_server_volume(vmuuid,cinderid)
					
				except:
					create_server_volume(vm,volume)
			

			def check_confirm(vm):
				try:
					vm.confirm_resize()
					print '1'
				except:
					check_confirm(vm)
						
			check_confirm(vm)
			#附加
			create_server_volume(vmuuid,cinderid)
			

			
			break

		if case(2):
			cinderid = volumes.get_server_volumes(vmuuid)[int(deviceidx)].volumeId
			tmpF = flavors.get(flavor_uuid)
			#resize
			try:
				vm.resize(tmpF)
			except:
				print 'resize fail'


			def check_confirm(vm):
				try:
					vm.confirm_resize()
					print '1'
				except:
					check_confirm(vm)
						
			check_confirm(vm)
			#附加
			volumes.delete_server_volume(vmuuid,cinderid)

			break

		if case(3):
			#擴充指定硬碟
		
			break


	# #若 diskCtrl = 0
 

	# flavors.delete(tmpF) #創立完VM後刪除
	return 1
def scanvm():
	vmuuid = '1d4cf234-0867-4a67-a713-6b06d5647c72'
	vm = servers.get(vmuuid)
	flavor_uuid = vm.flavor['id']
	VM_UUID = vm.id
	VM_Name = vm.name
	VM_CPUNum = flavors.get(flavor_uuid).vcpus
	VM_MemoryMB = flavors.get(flavor_uuid).ram
	VM_Status = vm._info['OS-EXT-STS:power_state']
	Host_UUID = vm._info['OS-EXT-SRV-ATTR:host']
	volume =  vm._info['os-extended-volumes:volumes_attached']
	vol_host_list = []
	for item in volume:
		volume = cinder.volumes.get(item['id'])
		# print volume
		vol_host = volume.__getattr__('os-vol-host-attr:host')

	SRUUID = vol_host
	item_array = {"VM_UUID":VM_UUID,"VM_Name":VM_Name,"VM_CPUNum":VM_CPUNum,"VM_MemoryMB":VM_MemoryMB,"VM_Status":VM_Status,"Host_UUID":Host_UUID,"SRUUID":SRUUID}
	return str(item_array)
def scandisk():
	output = ""
	vmuuid = '1d4cf234-0867-4a67-a713-6b06d5647c72'
	vm = servers.get(vmuuid)
	vm_vol =  vm._info['os-extended-volumes:volumes_attached']
	for item in vm_vol:
		VMDisk_UUID = item['id']
		# print item['id']
		volume = cinder.volumes.get(VMDisk_UUID)
		# print item['id']
		# print volume.id
		# print '---------'
		vol_host = volume.__getattr__('os-vol-host-attr:host')
		SRUUID= vol_host
		VMDisk_SizeGB = volume.size
		if not volume.name:
			VMDisk_Name=volume.id
		else:
			VMDisk_Name=volume.name
		if not volume.attachments:
			VM_UUID=''
			VMDisk_device=''
		else:
			VM_UUID = volume.attachments[0]['server_id']
			VMDisk_device = volume.attachments[0]['device']
		item_array = {"VM_UUID":VM_UUID,"VMDisk_UUID":VMDisk_UUID,"VMDisk_Name":VMDisk_Name,"SRUUID":SRUUID,"VMDisk_SizeGB":VMDisk_SizeGB,"VMDisk_device":VMDisk_device}
		# print item_array
		output += str(item_array)+"\n"
	# print output
	return str(output)
# ResourceModify()
f = open(Guid+'.txt', 'a')
f.write('[vm]\n')
f.write(scanvm())
f.write('\n')
f.write('[vmdisk]\n')
f.write(scandisk())
f.write('\n')
f.write('[END]\n')
f.close()

