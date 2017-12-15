# -*- coding: utf-8 -*-

from keystoneclient import session
from keystoneclient.v3 import client as keystoneclient
from keystoneclient.auth.identity import v3

from neutronclient.v2_0 import client as neutronclient
from cinderclient import client as cinderclient
from novaclient import client as novaclient
from glanceclient import glanceclient

api_version = 3
project_domain_id='default'
user_domain_id='default'


def _glance():
    glance = glanceclient.Client(2,session=sess)
    return glance

def _nova():
    nova = novaclient.Client(2,session=sess)
    return nova

def _cinder():
    cinder = cinderclient.Client(2,session=sess)
    return cinder

def _neutron():
    neutron = neutronclient.Client(session=sess)
    return neutron


def cinder(server_ip,server_account,server_pwd,project_name):
    server_address = 'http://'+server_ip+chooseAPI(api_version)
    auth = v3.Password(auth_url=server_address,username=server_account,password=server_pwd,project_name=project_name,project_domain_id=project_domain_id,user_domain_id=user_domain_id)
    # auth = v3.Password(auth_url='http://140.128.101.205:5000/v3',username='admin',password='1j6el4nj4su3',project_name='admin',project_domain_id='default',user_domain_id='default')
    sess = session.Session(auth=auth)
    cinder = cinderclient.Client(2,session=sess)
    return cinder

def glance(server_ip,server_account,server_pwd,project_name):
    server_address = 'http://'+server_ip+chooseAPI(api_version)
    auth = v3.Password(auth_url=server_address,username=server_account,password=server_pwd,project_name=project_name,
        project_domain_id=project_domain_id,user_domain_id=user_domain_id)
    # auth = v3.Password(auth_url='http://140.128.101.205:5000/v3',username='admin',password='1j6el4nj4su3',project_name='admin',project_domain_id='default',user_domain_id='default')
    sess = session.Session(auth=auth)
    glance = glanceclient.Client(2,session=sess)
    return glance

def nova(server_ip,server_account,server_pwd,project_name):

    server_address = 'http://'+server_ip+chooseAPI(api_version)
    auth = v3.Password(auth_url=server_address,username=server_account,password=server_pwd,project_name=project_name,project_domain_id=project_domain_id,user_domain_id=user_domain_id)
    # auth = v3.Password(auth_url='http://140.128.101.205:5000/v3',username='admin',password='1j6el4nj4su3',project_name='admin',project_domain_id='default',user_domain_id='default')
    sess = session.Session(auth=auth)
    nova = novaclient.Client(2,session=sess)
    return nova

def neutron(server_ip,server_account,server_pwd,project_name):
    server_address = 'http://'+server_ip+chooseAPI(api_version)
    auth = v3.Password(auth_url=server_address,username=server_account,password=server_pwd,project_name=project_name,project_domain_id=project_domain_id,user_domain_id=user_domain_id)
    # auth = v3.Password(auth_url='http://140.128.101.205:5000/v3',username='admin',password='1j6el4nj4su3',project_name='admin',project_domain_id='default',user_domain_id='default')
    sess = session.Session(auth=auth)
    neutron = neutronclient.Client(session=sess)
    return neutron

def chooseAPI(api_version):
    port = ':5000'
    if(api_version==2):
        return port+'/v2.0'
    elif(api_version ==3):
        return port+'/v3'
    else:
        return '0'



# server_ip = '140.128.101.205'
# api_version = 3
# server_account = 'admin'
# project_name ='admin'
# server_pwd = '1j6el4nj4su3'
# pool_name =''
# operator =''
# guid =''
# server_address = 'http://'+server_ip+chooseAPI(api_version)
# project_domain_id='default'
# user_domain_id='default'

# auth = v3.Password(auth_url=server_address,username=server_account,password=server_pwd,project_name=project_name,project_domain_id=project_domain_id,user_domain_id=user_domain_id)
# # auth = v3.Password(auth_url='http://140.128.101.205:5000/v3',username='admin',password='1j6el4nj4su3',project_name='admin',project_domain_id='default',user_domain_id='default')
# sess = session.Session(auth=auth)


