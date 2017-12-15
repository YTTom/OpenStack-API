import demjson
import client_setting

# nova = client.Client(2,'admin','1j6el4nj4su3','admin','http://140.128.101.205:5000/v2.0')
nova=client_setting.nova()
hl = nova.hypervisors.list()
hosts_dict=[]

for item in hl:
    Host_UUID =item.id
    Host_Name = item.hypervisor_hostname
    Host_IP =item.host_ip

    j=demjson.decode(item.cpu_info)
    CPU_count=j['topology']['cores']
    CPU_GHZ = 0
    CPU_Socket = j['topology']['sockets']
    MemoryMB=item.memory_mb
    #check hosts status

    PowerOn = 0
    if(item.status=='up'):
    	PowerOn = 1
    else:
    	PowerOn = 0
    #


	#
    item_array={'Host_UUID':Host_UUID,'Host_Name':Host_Name,'Host_IP':Host_IP,'CPU_Count':CPU_count,'CPU_GHZ':CPU_GHZ,'CPU_Socket':CPU_Socket,'MemoryMB':MemoryMB,'PowerOn':PowerOn} 
    hosts_dict.append(item_array)
    #

json =  demjson.encode(hosts_dict)
print(json)

