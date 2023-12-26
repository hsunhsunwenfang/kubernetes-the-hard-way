
import os


# Write a function to insert Host to ssh config
    
def insert_host_to_ssh_config(hostname, host, user, identityFilePath, ssh_config_file='~/.ssh/config'):

    from sshconf import read_ssh_config
    from os.path import expanduser

    # create ssh config file if not exists
    if not os.path.exists(expanduser(ssh_config_file)):
        with open(expanduser(ssh_config_file), 'w') as f:
            f.write("")
    
    c = read_ssh_config(expanduser(ssh_config_file))
    if host in c.hosts():
        print(f"Host {host} already exists in ssh config file")
    else:
        c.add(
            host=host,
            HostName=hostname,
            User=user,
            IdentityFile=identityFilePath
        )
        c.write(expanduser(ssh_config_file))