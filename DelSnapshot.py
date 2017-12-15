# -*- coding: utf-8 -*-
from novaclient import client
import client_setting
import sys
import io

argv = sys.argv[1]
Snapshot_id=sys.argv[2]
ServerIP=sys.argv[3]
ServerAccount=sys.argv[4]
ServerPwd=sys.argv[5]
PoolName=sys.argv[6]
Operator=sys.argv[7]
guid=sys.argv[8]
projectname=sys.argv[9]

nova = client_setting.nova(ServerIP,ServerAccount,ServerPwd,projectname)
flavors = nova.flavors
servers = nova.servers
hypervisors = nova.hypervisors
images = nova.images



def DelSnapshot(Snapshot_id):
	images.delete(images.get(Snapshot_id))


DelSnapshot(Snapshot_id)
print 1

