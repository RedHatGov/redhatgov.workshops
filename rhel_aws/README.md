# RHEL 8 Workshop - AWS Version

![rhel 8](img/Logo-Red_Hat-Enterprise_Linux_8-B-Standard-RGB.png)

`rhel8_aws` is a playbook to provision RHEL 8 in AWS. This playbook uses Ansible to provision AWS infrastructure and nodes.

These modules all require that you have AWS API keys available to use to provision AWS resources. You also need to have IAM permissions set to allow you to create resources within AWS. There are several methods for setting up your AWS environment, on you local machine.

This repo also requires that you have Ansible installed on your local machine. For the most upto date methods of installing Ansible for your operating system [check here](http://docs.ansible.com/ansible/intro_installation.html).

## Detailed AWS Infrastructure Creation Guides

#### OS X Catalina (10.15.x)

For easy installation and maintenance of the required tools, please first install [Homebrew](https://brew.sh/). From their site, the following command will install it to your system: 

```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Next, you need to install the required management tools, for Ansible and AWS:

```
$ brew install python3
$ pip3 install virtualenv
$ virtualenv ansible
$ source ansible/bin/activate
(ansible) $ pip install ansible boto boto3 awscli
(ansible) $ aws configure # fill out at least your AWS API keys, other variables are optional
(ansible) $ mkdir src
(ansible) $ cd src
(ansible) $ git clone https://github.com/RedHatGov/redhatgov.workshops.git
(ansible) $ cd ~/src/redhatgov.workshops/rhel_aws/
(ansible) $ cp group_vars/all_example.yml group_vars/all.yml
(ansible) $ vim group_vars/all.yml # fill in all the required fields
(ansible) $ ansible-playbook 1_provision.yml
(ansible) $ ansible-playbook 2_load.yml 
(ansible) $ ssh -i $(ls -1 .redhatgov/*-key | head -1) ec2-user@$(egrep '^workshop_prefix' group_vars/all.yml | awk -F\" '{ print $2 }').admin.redhatgov.io
(admin) $ cd src/rhel_aws
(admin) $ ansible-playbook 3_load.yml
```

#### RHEL 7

Unfortunately, the required Python modules are not available from the official repositories, so we will need to install them into a Python virtualenv, using pip:

```
$ sudo subscription-manager repos \
--enable rhel-7-server-ansible-2.8-rpms \
--enable rhel-7-server-optional-rpms \
--enable rhel-7-server-extras-rpms
$ sudo yum install -y git python-virtualenv ansible
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
(ansible) $ source env.sh
(ansible) $ ansible-playbook 1_provision.yml
(ansible) $ ansible-playbook 2_load.yml 
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
(ansible) $ source env.sh
(ansible) $ ansible-playbook 1_provision.yml
(ansible) $ ansible-playbook 2_load.yml 
```

#### Fedora 30/31/32
```
$ sudo dnf -y install git python3-boto python3-boto3 ansible awscli
$ aws configure # fill out at least your AWS API keys, other variables are optional
$ git clone https://github.com/RedHatGov/redhatgov.workshops.git
$ sed -i 's/env python/env python3/' inventory/hosts
$ cd ~/src/redhatgov.workshops/rhel_aws/
$ cp group_vars/all_example.yml group_vars/all.yml
$ vim group_vars/all.yml # fill in all the required fields
$ source env.sh
$ ansible-playbook 1_provision.yml
$ ansible-playbook 2_load.yml 
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

