# Ansible Tower Workshop

![ansible](img/Ansible-Tower-Logotype-Large-RGB-FullGrey-300x124.png)

`Ansible_Tower_Workshop` is a ansible playbook to provision Ansible Tower in Azure. This playbook uses Ansible to wrap Terraform, for provisioning Azure infrastructure and nodes. To find more info about Terraform [check here](https://www.terraform.io/docs/providers/azurerm/)

These modules all require that you have Azure ID's available to use to provision Azure resources. You also need to have Azure permissions set to allow you to create resources within Azure. There are several methods for setting up you Azure environment on you local machine.

Fill out `env.sh` & Export the Azure ID's

First, copy env.sh_example to env.sh, and then fill in your ID's.  Once that is complete, source the script, to export your Azure environment variables.

```
source env.sh
```

This repo also requires that you have Ansible installed on your local machine. For the most upto date methods of installing Ansible for your operating system [check here](http://docs.ansible.com/ansible/intro_installation.html).

This repo also requires that Terraform be installed if you are using the azure.infra.terraform role. For the most upto data methods of installing Terraform for your operating system [check here](https://www.terraform.io/downloads.html).



## Azure Infrastructure Roles


### roles/azure.infra.terraform

To create infrastructure and a Ansible Tower instance via Terraform:

**** OS X
```
sudo easy_install pip
sudo pip install boto
sudo pip install ansible
sudo pip install passlib
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew install terraform
```

**** RHEL/CentOS
```
sudo yum install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
# server
subscription-manager repos --enable="rhel-7-server-rpms" --enable="rhel-7-server-extras-rpms" --enable="rhel-7-server-optional-rpms"
# workstation
subscription-manager repos --enable="rhel-7-workstation-rpms" --enable="rhel-7-workstation-extras-rpms" --enable="rhel-7-workstation-optional-rpms"
sudo yum -y install python2-boto ansible
wget https://releases.hashicorp.com/terraform/0.9.11/terraform_0.9.11_linux_amd64.zip # current release as of this date...check to see if a newer version is availabke
sudo unzip terraform_0.9.11_linux_amd64.zip -d /usr/local/bin terraform
```

**** Fedora 25/26
```
sudo dnf -y install python2-boto ansible libselinux-python
wget https://releases.hashicorp.com/terraform/0.9.11/terraform_0.9.11_linux_amd64.zip # current release as of this date...check to see if a newer version is availabke
sudo unzip terraform_0.9.11_linux_amd64.zip -d /usr/local/bin terraform
```

First, copy group_vars/all_example to group_vars/all, and then edit `group_vars/all` and fill in the vars with your Azure api info. This role can also provide easy domain name mapping to all the instances if you have a domain registered in Azure. You can also update the number of tower instances to be created and the number of node instances to be created.


```
#####################################################
# Domain Name you own
#####################################################
domain_name: ""

#####################################################
# Azure ID's for terraform.tfvars file
#####################################################
azure_subscription_id:            ""
azure_client_id:                  ""
azure_client_secret:		          ""
azure_tenant_id:		              ""
```

## Configure Workshop Nodes
To call terraform to provision the nodes run the first playbook.

```
ansible-playbook 1_provision.yml
```
To install and configure the necessary software, on the newly created nodes, run the second playbook. It may be re-run as many times as necessary. The SUDO password is your local sudo password.

```
ansible-playbook 2_load.yml -K
```

To destroy

```
ansible-playbook 3_unregister.yml # only need to run this if you aren't using Cloud Access
cd .redhatgov
terraform destroy
```

```
```

## Login to Ansible Tower

Browse to the URL of the Azure instance and enter the `azure-user`'s password (workshop_password:) located in `group_vars/all`.

```
https://{{ workshop_prefix }}-tower0.{{ region }}.cloudapp.azure.com:8888/wetty/ssh/azure-user
```

![Tower Login](img/ansible-tower.png)

There is a web-based IDE running on port 8443 of each tower node.  That IDE can be used to edit Ansible playbooks, rather than using a command line editor, like `vim` or `nano`.

```
https://{{ workshop_prefix }}-tower0.{{ region }}.cloudapp.azure.com:8443
```

![Codiad Login](img/codiad.png)

## Walkthrough for Scripts

A walkthrough for most of the typewritten steps has been added to the workshop, both to speed up workshops presented within a limited schedule, or to help a studenmt who has made a mistake, or who has fallen far behind.

The walkthrough is deployed on the tower nodes, in `~azure-user/walkthrough`.
