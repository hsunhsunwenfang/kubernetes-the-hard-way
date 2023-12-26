


# Build VM

- Github Action for custom image
    - Link
        - MS Learn
            - https://learn.microsoft.com/en-us/azure/developer/github/build-vm-image?tabs=userlevel%2Cprincipal
        - Template
            - https://github.com/marketplace/actions/build-azure-virtual-machine-image#sample-workflow-to-create-a-custom-ubuntu-os-image-and-distribute-through-shared-image-gallery
        - All Github Action yaml configuration
            - https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#on

    - Configure Environment
        - https://learn.microsoft.com/en-us/entra/workload-id/workload-identity-federation-create-trust-user-assigned-managed-identity?pivots=identity-wif-mi-methods-azp#environment-example
    - Use OIDC [SUCCEEDED]
        - Flow
            - https://learn.microsoft.com/en-us/azure/developer/github/connect-from-azure?tabs=azure-portal%2Clinux#add-federated-credentials
        - Need to give Reader role on the Subscription to the MI
        - [Issue] but will fail if az version check goes first
            - https://github.com/hsunhsunwenfang/kubernetes-the-hard-way/actions/runs/7191115832
    - Use Managed Identity [FAILED]
        - Github official
            - https://github.com/marketplace/actions/azure-login
        - 3rd party simple way
            - https://yourazurecoach.com/2022/12/29/use-github-actions-with-user-assigned-managed-identity/
    - Use Self-hosted runner
        - Needed for Managed Identity login
            - https://github.com/marketplace/actions/azure-login#login-with-user-assigned-managed-identity
        - Start the self-hosted runner service [Omitted-at-first-but-crucial]
            - https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/configuring-the-self-hosted-runner-application-as-a-service?learn=hosting_your_own_runners&learnProduct=actions
    - Base Gallery Image
        - https://learn.microsoft.com/en-us/azure/virtual-machines/image-version?tabs=portal%2Ccli2
    - Culprit
        - RoleDefinitionLimitExceeded
            - Combine roles
                - But no roles has all this actions
            - Mitigation
                - Use Contributor for now
        - Unsupported region of federated credential
            - https://learn.microsoft.com/en-us/entra/workload-id/workload-identity-federation-considerations#unsupported-regions-user-assigned-managed-identities
            - Both the MI and it's RG should be compliant to the region supportability
        - Azure Login cannot work with MI or OIDC

- Create VMSS from custom image [TODO]
    - https://learn.microsoft.com/en-us/azure/virtual-machine-scale-sets/tutorial-use-custom-image-cli

- ssh-config for vmss
    - [TODO] store vmss ssh keys by az-cli scripting
    - [TODO] Configure .ssh/config by az-cli
        - Get vmss with tag
            - controllervmss=$(az vmss list --query "[?tags.node_type=='controller'].name" -otsv)
        - List instances
            -  az vmss list-instances -g kubernetes-the-hard-way -n $controllervmss
    - [TODO] Configure .ssh/config by az-python sdk
        - Get vmss with tag
            - controllervmss=$(az vmss list --query "[?tags.node_type=='controller'].name" -otsv)
        - List instances
            -  az vmss list-instances -g kubernetes-the-hard-way -n $controllervmss


# More

- AKS node and /opt/azure/vhd-install.complete
    - https://github.com/Azure/AKS/blob/master/vhd-notes/aks-ubuntu/AKSUbuntu-2204/202310.26.0.txt == /opt/azure/vhd-install.complete
    - [TODO] /opt/azure/tlsbootstrap
    - image related are in /opt/azure/containers

- cloud-init
    - github
        - https://github.com/canonical/cloud-init

- Azure Linux Agent waagent
    - Path in node
        - /var/lib/waagent/WALinuxAgent-2.9.1.1/bin/WALinuxAgent-2.9.1.1-py3.8.egg
    - Github
        - WALinuxAgent/azurelinuxagent at master · Azure/WALinuxAgent (github.com)
    - Remark
        - the .egg extension is simply a zip, we can rename .egg to .zip and unzip.
        - The unzipped folder will contains the azurelinuxagent folder that sits the cloud-init py scripts

# Reference

- Alex Github
    - https://github.com/alexxiongxiong/GoWebApp/blob/main/.github/workflows/main.yaml

