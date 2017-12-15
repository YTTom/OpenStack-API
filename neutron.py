from keystoneauth1 import identity
from keystoneauth1 import session
from neutronclient.v2_0 import client



#from pv import print_values
username='admin'
password='hpc123'
project_name='admin'
project_domain_id='default'
user_domain_id='default'
auth_url='http://172.23.2.200:5000/v3'
auth = identity.Password(auth_url=auth_url,username=username,password=password,project_name=project_name,project_domain_id=project_domain_id,user_domain_id=user_domain_id)
sess = session.Session(auth=auth)
neutron = client.Client(session=sess)

subnets = neutron.list_subnets()

#print getattr(subnets['subnets'],'service_types')
#print subnets['subnets'][0]['allocation_pools']
#print subnets['subnets'][1]['allocation_pools'][0]['start']
#print len(subnets['subnets'][1]['allocation_pools'][0])
print subnets['subnets'][0]['name']
print subnets['subnets'][0]['allocation_pools'][0]

print subnets['subnets'][1]['name']
print subnets['subnets'][1]['allocation_pools'][0]
#while i > 0:
   
 #   print(i)
  #  i -= 1 
  
  



