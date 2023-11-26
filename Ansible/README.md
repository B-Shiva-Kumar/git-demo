# Ansible:

* *It is a open source configuration management tool that automates deployement, orchestration, cloud provisioning and other tools.*
* *works on `push management`.*
* *It is agentless and works by connecting nodes through ssh.*
* *Uses YAML scripting.*
* *Scripts are called `playbooks`.*
* *One master can control many servers using ssh connection*


## Ansible Installation (ubuntu OS)

```
# installation

sudo apt update
sudo apt instal ansible
```

## Update all the node-servers from Ansible main-server

```
ansible all -m apt -a "upgrade=yes update_cache=yes cache_valid_time=86400" --become -i PATHTOINVENTORY --private-key=PRIVATEKEYPATH
```

* *Configure ssh private key*

    ```
    cd .ssh

    # copy-paste ansible private key (pem) in created ansible_key file
    vim ansible_key

    pwd  # /home/ubuntu/.ssh
    ```

* *to connect ssh (secured shell connection) from ANSIBLE-MASTER into Server-Node (Ansible-Node)*
    ```
    sudo ssh -i ~/.ssh/ansible_key ubuntu@<server-node-ip-addr>  # connect remotely to server-node specify ssh key and ip-address.

    exit   # logout
    ```

* *create ansible directory if not available after installation*

    ```
    cat /etc/ansible/hosts

    # if not available above dir. create one
    mkdir ansible

    cd ansible
    vim hosts  # hosts is a inveontry file (servers info)

    ```

* *add the below code to hosts (inventory file)*
    - this file contains all servers information
    - `[all:vars]` indicates to configure (python here) yby default

        ```
        [servers]
        server1 ansible_host=54.90.122.118
        server2 ansible_host=54.226.120.189
        server3 ansible_host=54.145.1.248


        # by default python must be install in all servers
        [all:vars]
        ansible_python_interpreter=/usr/bin/python3
        ```

    - to validate or show all servers info using inventory file
        ```
        # validate inventory file
        ansible-inventory --list -y -i /home/ubuntu/ansible/hosts
        ```

    - below OUTPUT show validated 
        ```
        # OUTPUT:

        all:
        children:
            servers:
            hosts:
                server1:
                ansible_host: 54.90.122.118
                ansible_python_interpreter: /usr/bin/python3
                server2:
                ansible_host: 54.226.120.189
                ansible_python_interpreter: /usr/bin/python3
                server3:
                ansible_host: 54.145.1.248
                ansible_python_interpreter: /usr/bin/python3
            ungrouped: {}
        ```


* *`test connection`* 
    - to ping all the servers using module (`-m`)*
    - module (-m) is a command or set of commands executed on client servers

        ```
        # To give permissions to .ssh and private-key
        # If no permissions throw unreachable ERROR

        chmod 700 ~/.ssh
        chmod 600 ~/.ssh/ansible_key
        ```

        ```
        # to ping all server using -m

        ansible all -m ping -i /home/ubuntu/ansible/hosts --private-key=~/.ssh/ansible_key
        ```

* *`check disk space / memory usage`* 
    - *to check memory usage of all the hosts from Ansible Master server*
        ```
        ansible all -a "free -f" -i /home/ubuntu/ansible/hosts --private-key=~/.ssh/ansible_key
        ```

* *`check all servers uptime`*
    ```
    ansible all -a "uptime" -i /home/ubuntu/ansible/hosts --private-key=~/.ssh/ansible_key
    ```
---

# Create and Deploy `Ansible Playbooks`:

* *`create a file` in all servers from `ansible_main` server*
    * *create a `playbooks` dir*
        ```
        mkdir playbooks
        ```

        * *ansible folder structure should look like this flow*
            - `/home/ubuntu/ansible`
                - `hosts` (file)
                - `playbooks` (folder)

    * *`deploy` a playbook*
        - `cd playbooks`
        - `vim create_file.yml`
        - add yaml script
            ```
            ---
            - name: This playbook will creata a file
            hosts: all
            become: true  # root user permission
            tasks:
                - name: create a file
                file:
                path: /home/ubuntu/main_file.txt
                state: touch

            ```
        - deploy `create_file.yml` playbook
            ```
            # pwd -> /home/ubuntu/ansible/playbooks

            ansible-playbook create_file.yml -i /home/ubuntu/ansible/hosts --private-key=~/.ssh/ansible_key
            ```

---

* *`create a user` in all servers*
    - `vim create_user.yml`
        ```
        ---
        - name: this playbook will create a user
          hosts: all
          become: true
          tasks:
          - name: To create a user name shiva
            # module to create a user
            user: name=shiva
        ```
    - *`deploy` playbook*
        ```
        ansible-playbook create_user.yml -i /home/ubuntu/ansible/hosts --private-key=~/.ssh/ansible_key
        ```
    - *`OUTPUT: changed=1`*
        ```
        ubuntu@ip-172-31-16-206:~/ansible/playbooks$ ansible-playbook create_user.yml -i /home/ubuntu/ansible/hosts --private-key=~/.ssh/ansible_key

        # OUTPUT
        PLAY [this playbook will create a user] ******************************************************************************************************************************************************

        TASK [Gathering Facts] ***********************************************************************************************************************************************************************
        ok: [server1]
        ok: [server3]
        ok: [server2]

        TASK [To create a user name shiva] ***********************************************************************************************************************************************************
        changed: [server1]
        changed: [server3]
        changed: [server2]

        PLAY RECAP ***********************************************************************************************************************************************************************************
        server1                    : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
        server2                    : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
        server3                    : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
        ```
    
    - *`OUTPUT: changed=0` -> run/deploy the same command/playbook -> logs in PLAY  RECAP show `changed=0`*
        - this is because we already ran the ansible create user playbook and user `shiva` already exists in all servers
        ```
        ubuntu@ip-172-31-16-206:~/ansible/playbooks$ ansible-playbook create_user.yml -i /home/ubuntu/ansible/hosts --private-key=~/.ssh/ansible_key

        PLAY [this playbook will create a user] ******************************************************************************************************************************************************

        TASK [Gathering Facts] ***********************************************************************************************************************************************************************
        ok: [server2]
        ok: [server1]
        ok: [server3]

        TASK [To create a user name shiva] ***********************************************************************************************************************************************************
        ok: [server2]
        ok: [server3]
        ok: [server1]

        PLAY RECAP ***********************************************************************************************************************************************************************************
        server1                    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
        server2                    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
        server3                    : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
        ```

    - *`verify` user created*
        - `sudo ssh -i ~/.ssh/ansible_key ubuntu@ip-address`
        ```
        ubuntu@ip-172-31-25-114:~$ cat /etc/passwd
        .
        .
        .
        lxd:x:999:100::/var/snap/lxd/common/lxd:/bin/false
        shiva:x:1001:1001::/home/shiva:/bin/sh
        ```
---

# Automate installation of docker in all the servers using `Ansible playbook`

* *create `install_docker.yml` playbook*
    - automating installation of docker in all the servers using the below playbook
    ```
    ---
    - name: This playbook will install Docker
    hosts: all
    become: true
    tasks:
    - name: Add Docker GPG apt Key
        apt_key:
        url: https://download.docker.com/linux/ubuntu/gpg
        state: present

    - name: Add Docker Repository
        apt_repository:
        repo: deb https://download.docker.com/linux/ubuntu focal stable
        state: present

    - name: Install Docker
        apt:
        name: docker-ce
        state: latest
    ```
    - *`run / deploy` playbook*
        ```
        # ensure to update all the servers to avoid installation failures before playbook deploy

        ansible-playbook install_docker.yml -i /home/ubuntu/ansible/hosts --private-key=~/.ssh/ansible_key
        ```

---