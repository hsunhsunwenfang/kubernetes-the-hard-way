

az login --identity

worker_vms=$(az vmss list-instances -g kubernetes-the-hard-way -n worker-vmss --query "[].instanceId" -otsv)
worker_vm_arr=($(echo $worker_vms | tr '\n' ' '))

controller_vms=$(az vmss list-instances -g kubernetes-the-hard-way -n controller-vmss --query "[].instanceId" -otsv)
controller_vm_arr=($(echo $controller_vms | tr '\n' ' '))

