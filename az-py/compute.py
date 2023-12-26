
import argparse
import os
import sys
import time
import datetime
import json
import re
import requests
import yaml
import logging
import logging.config


from azure.identity import ManagedIdentityCredential, ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient

# python function using python sdk to achieve az login --identity

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

from utils import insert_host_to_ssh_config

class AzCredClient:
    def __init__(self, tenant_id, subscription_id):
        self.tenant_id = tenant_id
        self.subscription_id = subscription_id
        self.endpoint = "https://management.azure.com"

    def get_az_cred(self):
        # print(ManagedIdentityCredential())
        return ManagedIdentityCredential()
        
    def get_resource_by_restapi(self, url, api_version='2023-07-01'):

        token = self.get_az_cred().get_token(f'{self.endpoint}/.default').token
        
        # url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/microsoft.Compute/virtualMachineScaleSets/{vmss_name}/networkInterfaces"
        params = {'api-version': api_version}
        request = requests.Request('GET', url, params=params)
        prepped = request.prepare()
        prepped.headers['Authorization'] = f'Bearer {token}'

        with requests.Session() as session:
            response = session.send(prepped )

            if( response.status_code == 200 ):
                return json.loads(response.text)
            else:
                print(response.status_code)
                logger.error(f"Failed to communicate with api service: HTTP {response.status_code} - {response.text}")
                return None

    def get_az_compute_client(self):
        return ComputeManagementClient(
            self.get_az_cred()._credential,
            self.subscription_id
        )
    
# get all vmss with tag 'node_type' and value 'controller'

def get_vmss_list(az_client, resource_group, node_type):
    vmss_filtered = []
    vmss_list = az_client.virtual_machine_scale_sets.list(resource_group)
    for vmss in vmss_list:
        if isinstance(vmss.tags,dict)  and vmss.tags['node_type'] == node_type:
            vmss_filtered.append(vmss.name)
    return vmss_filtered

def get_vmss_vm_ip_dict(az_cred_client, vmss_name, resource_group):
    subscription_id = az_cred_client.subscription_id
    vmss_vm_url = f"{az_cred_client.endpoint}/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/microsoft.Compute/virtualMachineScaleSets/{vmss_name}/virtualMachines"
    vmss_vms = az_cred_client.get_resource_by_restapi(vmss_vm_url)

    # print(vmss_vms)
    vmss_ip_dict = {}
    for vm in vmss_vms['value']:
        vm_url = f"{az_cred_client.endpoint}{vm['id'].replace(f'virtualMachineScaleSets/{vmss_name}/', '')}"
        vm_json = az_cred_client.get_resource_by_restapi(vm_url)
        vm_nic_id = vm_json['properties']['networkProfile']['networkInterfaces'][0]['id']
        vm_nic_url = f"{az_cred_client.endpoint}{vm_nic_id}"
        vm_ip = az_cred_client.get_resource_by_restapi(f"{az_cred_client.endpoint}{vm_nic_id}", api_version='2023-05-01')['properties']['ipConfigurations'][0]['properties']['privateIPAddress']
        vmss_ip_dict[vm['name']] = vm_ip
    
    return vmss_ip_dict
        
def insert_k8s_worker_to_ssh_config(az_cred_client, azure_username, identity_file, resource_group="kubernetes-the-hard-way"):
    az_client = az_cred_client.get_az_compute_client()
    worker_vmss = get_vmss_list(az_client, "kubernetes-the-hard-way", "worker")[0]
    vmss_ip_dict = get_vmss_vm_ip_dict(az_cred_client, worker_vmss, resource_group)
    for vm_name in vmss_ip_dict:
        insert_host_to_ssh_config(vm_name, vmss_ip_dict[vm_name], azure_username, identity_file)

def insert_k8s_controller_to_ssh_config(az_cred_client, azure_username, identity_file, resource_group="kubernetes-the-hard-way"):
    az_client = az_cred_client.get_az_compute_client()
    controller_vmss = get_vmss_list(az_client, "kubernetes-the-hard-way", "controller")[0]
    vmss_ip_dict = get_vmss_vm_ip_dict(az_cred_client, controller_vmss, resource_group)
    for vm_name in vmss_ip_dict:
        insert_host_to_ssh_config(vm_name, vmss_ip_dict[vm_name], azure_username, identity_file)

def test_insert_k8s_worker_to_ssh_config():
    az_cred_client = AzCredClient('72f988bf-86f1-41af-91ab-2d7cd011db47', '2aa714e3-5fa4-45b2-9e3f-88f8eb04588c')
    insert_k8s_worker_to_ssh_config(az_cred_client, "hsunwen", "~/.ssh/keys/worker_key.pem")
    insert_k8s_controller_to_ssh_config(az_cred_client, "hsunwen", "~/.ssh/keys/controller_key.pem")

if __name__ == '__main__':

    test_insert_k8s_worker_to_ssh_config()

    pass