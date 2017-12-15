# -*- coding: utf-8 -*-
from novaclient import client
import client_setting
import globalFunction as gf
# import autoScan 
import time
import sys
import io

# credentials = get_nova_credentials()
# nova_client = nvclient.Client(**credentials)

# Replace with server_id and network_id from your environment
serverip = "140.128.101.205"
serveraccount = "admin"
serverpwd = "1j6el4nj4su3"
pool_name = "admin"
cinder = client_setting.cinder(serverip,serveraccount,serverpwd,pool_name)
nova = client_setting.nova(serverip,serveraccount,serverpwd,pool_name)
neutron = client_setting.neutron(serverip,serveraccount,serverpwd,pool_name)

server_id = 'b0e459a9-18ec-4c74-9ecf-e59fab5af8bf'
network_id = 'c10f757e-14ec-40f0-9714-41fb902b6163'
# server_detail = nova_client.servers.get(server_id)
body_value = {
                "port": {
                        "admin_state_up": True,
                        "name": "port1",
                        "network_id": network_id,
                        "fixed_ips":[
          				 			{
               						"subnet_id": "81f971eb-d350-476e-9259-d7a013d214b4"
            						}
      								],

                      }
                 }
response = neutron.create_port(body=body_value)
print response['port']['id']
