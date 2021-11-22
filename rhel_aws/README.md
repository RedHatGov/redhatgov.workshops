# RHEL 8 Workshop - AWS Version

![rhel 8](img/Logo-Red_Hat-Enterprise_Linux_8-B-Standard-RGB.png)

`rhel8_aws` is a playbook to provision RHEL 8 in AWS. This playbook uses Ansible to provision AWS infrastructure and nodes.

These modules all require that you have AWS API keys available to use to provision AWS resources. You also need to have IAM permissions set to allow you to create resources within AWS. There are several methods for setting up your AWS environment, on you local machine.

This repo also requires that you have Ansible installed on your local machine. For the most upto date methods of installing Ansible for your operating system [check here](http://docs.ansible.com/ansible/intro_installation.html).

## Valid AWS regions

By default this workshop is deployed in AWS region us-east-2 (Ohio).

The available regions for the RHEL 8 workshop are:
- us-east-2 (Ohio)
- us-east-1 (N. Virginia)
- ap-southeast-2 (Sydney)

This is based on a dependency for the correct AWS AMIs being defined for the region in roles/aws.create/defaults/main.yml

Please refer to the configuration instructions below for further information

## Detailed AWS Infrastructure Creation Guides

#### Mac OS 10.15.x+

For easy installation and maintenance of the required tools, please first install [Homebrew](https://brew.sh/). From their site, the following command will install it to your system: 

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Next, you need to install the required management tools, for Ansible and AWS:

```
$ brew install python3 socat gnu-tar openssl
$ pip3 install virtualenv
$ python3 -m venv ansible
$ source ansible/bin/activate
(ansible) $ ln -s /usr/local/bin/gtar ~/ansible/bin/tar
(ansible) $ ln -s /usr/local/opt/openssl@3/bin/openssl ~/ansible/bin/
(ansible) $ pip install ansible boto boto3 awscli passlib
```

*NOTE*: If you get an error building any of these python packages, then you probably should upgrade pip:
```
(ansible) $ python3 -m pip install --upgrade pip
(ansible) $ pip install ansible boto boto3 awscli passlib
```

Continuing:

```
(ansible) $ aws configure # fill out at least your AWS API keys, other variables are optional
(ansible) $ mkdir ~/src
(ansible) $ cd ~/src
(ansible) $ git clone https://github.com/RedHatGov/redhatgov.workshops.git
(ansible) $ cd ~/src/redhatgov.workshops/rhel_aws/
(ansible) $ cp group_vars/all_example.yml group_vars/all.yml
(ansible) $ vim group_vars/all.yml # fill in all the required fields
(ansible) $ ansible-galaxy collection install ansible.posix
(ansible) $ ansible-galaxy collection install community.aws
(ansible) $ ansible-galaxy install geerlingguy.swap
(ansible) $ export AWS_PROFILE=default # or whatever your aws profile is called
(ansible) $ ansible-playbook 1_provision.yml
```

*NOTE* if you get an error about python modules, like boto and boto3, being missing, your system is using the wrong Python instance. Do this:

```
(ansible) $ sed -i "s+^localhost.*+localhost  ansible_connection=local ansible_python_interpreter=`which python3`+" inventory/hosts
(ansible) $ ansible-playbook 1_provision.yml
```

And continue:

```
(ansible) $ ansible-playbook 2_load.yml 
(ansible) $ ansible-playbook 2a_fix.yml 
```

#### RHEL 7

Unfortunately, the required Python modules are not available from the official repositories, so we will need to install them into a Python virtualenv, using pip:

```
$ sudo yum install -y git python3 python3-pip python3-wheel
$ python3 -m venv ansible
$ source ansible/bin/activate
(ansible) $ pip install --upgrade pip
(ansible) $ pip install ansible boto boto3 awscli
(ansible) $ aws configure # fill out at least your AWS API keys, other variables are optional
(ansible) $ mkdir src
(ansible) $ cd src/
(ansible) $ git clone https://github.com/RedHatGov/redhatgov.workshops.git
(ansible) $ cd ~/src/redhatgov.workshops/rhel_aws/
(ansible) $ cp group_vars/all_example.yml group_vars/all.yml
(ansible) $ vim group_vars/all.yml # fill in all the required fields
(ansible) $ ansible-galaxy collection install ansible.posix
(ansible) $ ansible-galaxy collection install community.aws
(ansible) $ ansible-galaxy install geerlingguy.swap
(ansible) $ export AWS_PROFILE=default # or whatever your aws profile is called
(ansible) $ ansible-playbook 1_provision.yml
```

*NOTE* if you get an error about python modules, like boto and boto3, being missing, your system is using the wrong Python instance. Do this:

```
(ansible) $ sed -i "s+^localhost.*+localhost  ansible_connection=local ansible_python_interpreter=`which python3`+" inventory/hosts
(ansible) $ ansible-playbook 1_provision.yml
```

And continue:

```
(ansible) $ ansible-playbook 2_load.yml 
(ansible) $ ansible-playbook 2a_fix.yml 
```

#### RHEL 8

Unfortunately, the required Python modules are not available from the official repositories, so we will need to install them into a Python virtualenv, using pip:

```
$ sudo subscription-manager repos --enable ansible-2.9-for-rhel-8-x86_64-rpms --enable codeready-builder-for-rhel-8-x86_64-rpms
$ sudo dnf install -y git python3-virtualenv ansible
$ virtualenv --system-site-packages ansible
$ source ansible/bin/activate
(ansible) $ pip install boto boto3 awscli
(ansible) $ aws configure # fill out at least your AWS API keys, other variables are optional
(ansible) $ mkdir src
(ansible) $ cd src/
(ansible) $ git clone https://github.com/RedHatGov/redhatgov.workshops.git
(ansible) $ cd ~/src/redhatgov.workshops/rhel_aws/
(ansible) $ cp group_vars/all_example.yml group_vars/all.yml
(ansible) $ vim group_vars/all.yml # fill in all the required fields
(ansible) $ ansible-galaxy collection install ansible.posix
(ansible) $ ansible-galaxy collection install community.aws
(ansible) $ ansible-galaxy install geerlingguy.swap
(ansible) $ ansible-playbook 1_provision.yml
(ansible) $ ansible-playbook 2_load.yml 
(ansible) $ ansible-playbook 2a_fix.yml 
```

#### Fedora 30/31/32/33/34/35
```
$ sudo dnf -y install git python3-boto python3-boto3 ansible awscli
$ aws configure # fill out at least your AWS API keys, other variables are optional
$ git clone https://github.com/RedHatGov/redhatgov.workshops.git
$ sed -i 's/env python/env python3/' inventory/hosts _(probably not relevant any longer)_
$ cd ~/src/redhatgov.workshops/rhel_aws/
$ cp group_vars/all_example.yml group_vars/all.yml
$ vim group_vars/all.yml # fill in all the required fields
$ ansible-galaxy collection install ansible.posix
$ ansible-galaxy collection install community.aws
$ ansible-galaxy install geerlingguy.swap
$ ansible-playbook 1_provision.yml
$ ansible-playbook 2_load.yml 
$ ansible-playbook 2a_fix.yml 
```

#### Containerised build environment as non-root user

Pre-requisites: Linux host with podman installed

From Linux host (as regular non-root user)
```
$ podman run -dt -v $(pwd):/src:Z quay.io/rhn_sa_bblasco/build_rhel8_workshop:latest
$ podman ps -a
$ podman exec -it <container name from previous command> /bin/bash
```

Once inside the container (as root user)
```
[root@3beb48b4e1cf /]# export USER=root
[root@3beb48b4e1cf /]# cd /root
[root@3beb48b4e1cf /]# git clone https://github.com/RedHatGov/redhatgov.workshops.git
[root@3beb48b4e1cf /]# cd redhatgov.workshops/rhel_aws
[root@3beb48b4e1cf /]# cp -p group_vars/all_example.yml group_vars/all.yml # fill in all the required fields
[root@3beb48b4e1cf /]# aws configure # Fill in keys, default region

[root@3beb48b4e1cf /]# unbuffer ansible-playbook 1_provision.yml -v | tee 1_provision-$(date +%Y-%m-%d.%H%M).log 2>&1
[root@3beb48b4e1cf /]# unbuffer ansible-playbook 2_load.yml -v | tee 2_load-$(date +%Y-%m-%d.%H%M).log 2>&1
[root@3beb48b4e1cf /]# unbuffer ansible-playbook 2a_fix.yml -v | tee 2a_fix-$(date +%Y-%m-%d.%H%M).log 2>&1
```
Remove hosts etc. when workshop is finished
```
[root@3beb48b4e1cf /]# unbuffer ansible-playbook 3_unregister.yml -v | tee 3_unregister-$(date +%Y-%m-%d.%H%M).log 2>&1
```

#### Custom Variable Requirements
* Copy `group_vars/all_example.yml` to `group_vars/all.yml`
* Fill in the following fields:
```
  workshop_prefix  : defaults to "tower", set to the name of your workshop
  jboss            : defaults to "true", comment out to disable jboss
  graphical        : defaults to "true", change it to false if you don't want a graphical desktop for students to run Microsoft VS Code from
  aws_access_key   : your Amazon AWS API key
  aws_secret_key   : your Amazon AWS secret key
  domain_name      : your DNS domain, likely "redhagov.io"
  zone_id:         : the AWS Route 53 zone ID for your domain
  tower_rhel_count : the number of tower instances, usually 1 per student
  rhel_count       : the number of regular RHEL instances, usually 1 per student
  win_count        : the number of Windows 2016 instances, currently not used
  region:          : defaults to "us-east-2", set to any region
  rhel_ami_id      : defaults to "us-east-2" AMIs, uncomment us-east-1, or add your preferred region, as desired.  There are both JBoss-enabled and plain RHEL instances avalable
  win_ami_id       : similarly to "rhel_ami_id", uncomment to match your region choice
  workshop_passwoed: pick a password for your students to login with
  rabbit_password  : pick a password for RabbitMQ in Tower, usually not needed
  local_user       : if you are using a Mac, uncomment the Mac-specific entry, and comment the RHEL/Fedora one
```

**IMPORTANT!:**
For the Maven/JBoss steps in Exercise 1.0 to work, you must have a JBoss-enabled Cloud Access AMI, or you must disable Cloud Access, and use a traditional subscription, as shown below.  It is recommended that you enable Cloud Access and NOT use a traditional subscription as there is a known/unresolved bug when connecting to Red Hat servers.  
While logged into AWS Console, under Images click on 'AMIs', click on dropdown next to search bar and select 'Private Images'. Search for 'EAP' and use the AMI ID for the most recent release of RHEL.

**NOTE: If following this recommendation, your variables will look like this:**

```
# subscription_manager     |      Red Hat Subscription via Cloud Access
cloud_access:                     true
# subscription_manager     |      Red Hat Subscription via activation key and org id
rhsm_activationkey:               ""
rhsm_org_id:                      ""
# subscription_manager     |      Red Hat Subscription via username & password
username:                         ""
password:                         ""
pool_id:                          ""
```
**NOTE: If you choose the traditional RHSM route, your variables will look something like this**

Red Hat Subscription Manager uses **_either_** an `activation key / org id` combination or a `username/password` combination, not both.
```
# subscription_manager     |      Red Hat Subscription via Cloud Access
cloud_access:                     false
# subscription_manager     |      Red Hat Subscription via activation key and org id
rhsm_activationkey:               "myactkey"
rhsm_org_id:                      "12345678"
# subscription_manager     |      Red Hat Subscription via username & password
username:                         "user@company.com"
password:                         "my_password"
pool_id:                          "1234567890abcdef01234567890abcde"
```

#### Provision Workshop Nodes

```
source env.sh
ansible-playbook 1_provision.yml  
```
#### Install packages and configure the newly provisioned nodes.

```
ansible-playbook 2_load.yml
(login to admin node as ec2-user)
cd ~/src/rhel_aws)
ansible-playbook 3_load.yml
```

#### To destroy the workshop environment

```
ansible-playbook 4_unregister.yml
rm -rf .redhatgov
```

## Login to the primary workshop node

Browse to the URL of the EC2 instance and enter the `ec2-user`'s password `workshop_password:` located in `group_vars/all.yml`.

```
https://{{ workshop_prefix }}.tower.0.{{ domain_name }}:8888/wetty/ssh/ec2-user
```

## Alternative interface: RDP (Microsoft Remote Desktop)

Users of the workshop can, alternatively, login to the Tower nodes, using a Microsoft Remote Desktop (RDP) client.  This service is running on the standard port of 3389.  Once in, you will have a GNOME graphical session, with Microsoft Vidual Studio Code and the Firefox browser, to do the workshop.  All Wetty terminal commands can be entered into the GNOME terminal, and will work the same way.  Copy and paste functionality is verified using Microsoft's official client, and using Remmina, from Fedora.

