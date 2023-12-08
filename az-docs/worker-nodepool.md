


- Github Action for custom image
    - Link
        - MS Learn
            - https://learn.microsoft.com/en-us/azure/developer/github/build-vm-image?tabs=userlevel%2Cprincipal
        - Template
            - https://github.com/marketplace/actions/build-azure-virtual-machine-image#sample-workflow-to-create-a-custom-ubuntu-os-image-and-distribute-through-shared-image-gallery
    - Base Gallery Image
        - https://learn.microsoft.com/en-us/azure/virtual-machines/image-version?tabs=portal%2Ccli2
    - Culprit
        - RoleDefinitionLimitExceeded
            - Combine roles
                - But no roles has all this actions
            - Use Contributor for now
        - Unsupported region of federated credential
            - https://learn.microsoft.com/en-us/entra/workload-id/workload-identity-federation-considerations#unsupported-regions-user-assigned-managed-identities
            - Both the MI and it's RG should be compliant to the region supportability
- Create VMSS from custom image
    - https://learn.microsoft.com/en-us/azure/virtual-machine-scale-sets/tutorial-use-custom-image-cli


- AKS node and /opt/azure/vhd-install.complete
    - https://github.com/Azure/AKS/blob/master/vhd-notes/aks-ubuntu/AKSUbuntu-2204/202310.26.0.txt == /opt/azure/vhd-install.complete
    - [TODO] /opt/azure/tlsbootstrap
    - image related are in /opt/azure/containers