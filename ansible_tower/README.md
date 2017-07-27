# Ansible Tower Workshop

![ansible](img/Ansible-Tower-Logotype-Large-RGB-FullGrey-300x124.png)

`Ansible_Tower_Workshop` is a ansible playbook to provision Ansible Tower in AWS. This playbook uses Ansible to wrap Terraform, for provisioning AWS infrastructure and nodes. To find more info about Terraform [check here](https://www.terraform.io/docs/providers/aws/index.html)

These modules all require that you have AWS API keys available to use to provision AWS resources. You also need to have IAM permissions set to allow you to create resources within AWS. There are several methods for setting up you AWS environment on you local machine.

Fill out `env.sh` & Export the AWS API Keys ;

```
source env.sh
```

This repo also requires that you have Ansible installed on your local machine. For the most upto date methods of installing Ansible for your operating system [check here](http://docs.ansible.com/ansible/intro_installation.html).

This repo also requires that Terraform be installed if you are using the aws.infra.terraform role. For the most upto data methods of installing Terraform for your operating system [check here](https://www.terraform.io/downloads.html).



## AWS Infrastructure Roles


### roles/aws.infra.terraform

To create infrastructure and a Ansible Tower instance via Terraform:

**** OS X
```
sudo easy_install pip
sudo pip install boto
sudo pip install ansible
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
sudo dnf -y install python2-boto ansible
wget https://releases.hashicorp.com/terraform/0.9.11/terraform_0.9.11_linux_amd64.zip # current release as of this date...check to see if a newer version is availabke
sudo unzip terraform_0.9.11_linux_amd64.zip -d /usr/local/bin terraform
```

Then edit `group_vars/all` and fill in the vars with your AWS api info. This role can also provide easy domain name mapping to all the instances if you have a domain registered in AWS Route 53. 

Also, edit `2_configure.yml` and `3_unregister.yml`, and replace the "changeme" tag with the workshop name that you added to the `group_vars/all` file.


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

```
ansible-playbook -i inventory 1_provision.yml  
```

To destroy

```
cd .terraform
terraform destroy
```

## Configure Workshop Nodes


To target the newly created EC2 instance use the `ec2.py` module located in the `/inventory/` folder. The [ec2.py](http://docs.ansible.com/ansible/intro_dynamic_inventory.html) is a dynamic script that queries Amazon for your instances. 


```
ansible-playbook -i inventory 2_aws_ec2.yml
```

## Login to Ansible Tower

Browse to the URL of the EC2 instance and enter the `ec2-user`'s password (workshop_password:) located in `group_vars/all`. 

```
https://{{ workshop_prefix }}.tower.0.{{ domain_name }}:8888/wetty/ssh/ec2-user
```

![Login](img/ansible-tower.png)



