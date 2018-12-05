# Containers 101 Workshop

![ansible](img/Ansible-Tower-Logotype-Large-RGB-FullGrey-300x124.png)

`containers_101` is an ansible playbook to provision student container host nodes in AWS. This playbook uses Ansible to wrap Terraform, for provisioning AWS infrastructure and nodes. To find more info about Terraform [check here](https://www.terraform.io/docs/providers/aws/index.html)

These modules all require that you have AWS API keys available to use to provision AWS resources. You also need to have IAM permissions set to allow you to create resources within AWS. There are several methods for setting up you AWS environment on you local machine.

Fill out `env.sh` & Export the AWS API Keys

First, copy env.sh_example to env.sh, and then fill in your API keys.  Once that is complete, source the script, to export your AWS environment variables.

```
source env.sh
```

This repo also requires that you have Ansible installed on your local machine. For the most upto date methods of installing Ansible for your operating system [check here](http://docs.ansible.com/ansible/intro_installation.html).

This repo also requires that Terraform be installed if you are using the aws.infra.terraform role. For the most upto data methods of installing Terraform for your operating system [check here](https://www.terraform.io/downloads.html).



## AWS Infrastructure Roles


### roles/aws.infra.terraform

To create infrastructure and a Ansible Tower instance via Terraform:

#### OS X
```
sudo easy_install pip
sudo pip install boto
sudo pip install ansible
sudo pip install passlib
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew install terraform
```

#### RHEL/CentOS
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

#### Fedora 25/26/27/28/29
```
sudo dnf -y install python2-boto ansible python3-botocore python3-boto python3-boto3
wget https://releases.hashicorp.com/terraform/0.11.7/terraform_0.11.7_linux_amd64.zip # current release as of this date...check to see if a newer version is availabke
sudo unzip terraform_0.11.7_linux_amd64.zip -d /usr/local/bin terraform
```

Then edit `group_vars/all` and fill in the vars with your AWS api info. This role can also provide easy domain name mapping to all the instances if you have a domain registered in AWS Route 53.  You can get the zone ID from the DNS domain stored in Route 53.


```
#####################################################
# Domain Name you own
#####################################################
domain_name: ""
zone_id: ""

#####################################################
# AWS API Keys for terraform.tfvars file
#####################################################
aws_access_key: ""
aws_secret_key: ""
```

#### Configure Workshop Nodes

To install and configure the necessary software, on the newly created nodes, run the second playbook.  It may be re-run as many times as necessary.

```
ansible-playbook 1_provision.yml  
ansible-playbook 2_load.yml -K
```

#### To destroy the workshop environment

```
ansible-playbook 3_unregister.yml 
rm -rf .redhatgov
```

## Login to Wetty

Browse to the URL of the EC2 instance and enter the `ec2-user`'s username and password (workshop_password:) located in `group_vars/all`. 

```
https://{{ workshop_prefix }}.node.0.{{ domain_name }}:8888/wetty/ssh/ec2-user
```

![Tower Login](img/ansible-tower.png)

There is a web-based IDE running on port 8443 of each tower node.  That IDE can be used to edit Ansible playbooks, rather than using a command line editor, like `vim` or `nano`.

![Codiad Login](img/codiad.png)

## Walkthrough for Scripts

A walkthrough for most of the typewritten steps has been added to the workshop, both to speed up workshops presented within a limited schedule, or to help a studenmt who has made a mistake, or who has fallen far behind.

The walkthrough is deployed on the tower nodes, in `~ec2-user/walkthrough`.

