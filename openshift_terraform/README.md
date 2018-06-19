# OpenShift Terraform

This Ansible playbook is used to install OpenShift on Terraform supported providers.  Out of the box this playbook will create a three node OpenShift cluster with a Master and two OpenShift nodes on Amazon EC2 instances in the AWS cloud.  Future versions of this playbook will enable more providers.  This playbook can be modified to increase the number of nodes in the cluster if so desired.

After checking out this repository, search for the string "INSERT_VALUES_HERE" through out the files and replace that string with the appropriate values for the field.  The files and fields that need this change are listed below.

# Dependencies

- [Terraform](https://www.terraform.io/intro/getting-started/install.html) (v0.8.5)
- [Ansible](http://docs.ansible.com/ansible/intro_installation.html) (v2.2.1.0)
- [Red Hat Customer Portal Activation Key](https://access.redhat.com/articles/1378093)
- [Red Hat Cloud Access](https://www.redhat.com/en/technologies/cloud-computing/cloud-access) (optional)

### [Amazon Web Services](https://access.redhat.com/articles/2623521)

- [AWS Command Line Interface](http://docs.aws.amazon.com/cli/latest/userguide/installing.html)
- Domain purchased through AWS and managed by [Route53](https://aws.amazon.com/route53/)

### [Google Cloud Platform](https://access.redhat.com/articles/2751521)

- TBD

### Microsoft Azure

- TBD

# Required

The following variables must be set before usage.



### group_vars/all/vault.yml

The first two values are the DNS domain name (often `redhatgov.io`) and the cluster name, which will form the DNS subdomain:

```
vault_default_domain: "${INSERT_VALUE_HERE}"
vault_cluster_name:   "${INSERT_VALUE_HERE}"
```

Next, insert your AWS access and secret access keys, just as you did in `env.sh`:

```
vault_aws_access_key_id:     "${INSERT_VALUE_HERE}"
vault_aws_secret_access_key: "${INSERT_VALUE_HERE}"
```

The next value can be obtained from the AWS Route53 GUI, or by using the command below the example:

```
vault_aws_route53_zone_id: "${INSERT_VALUE_HERE}"
```
The `aws_route53_zone_id` value can be found using the following command:

<pre>
aws route53 list-hosted-zones --query 'HostedZones[*]' --output text | \
grep '\/hostedzone\/.*<b>${INSERT_VALUE_HERE}</b>' | sed -e 's/.*\///' -e 's/[^a-zA-Z0-9].*//'
</pre>

Make sure to replace `${INSERT_VALUE_HERE}` with the domain purchased through AWS and managed by Route53.

Next, set an activation key (which needs to be created in RHSM), and it's accompanying Org ID:

```
rhel_rhsm_activationkey: "${INSERT_VALUE_HERE}"
rhel_rhsm_org_id: "${INSERT_VALUE_HERE}"
```

Last, define what you want the OpenShift admin user and password to be:

```
vault_openshift_cluster_admin_username: "${INSERT_VALUE_HERE}"
vault_openshift_cluster_admin_password: "${INSERT_VALUE_HERE}"
```

You also need to update the `vault_number_nodes` variable in `group_vars/all/vault.yml` to reflect the desired number of nodes, if you want more than the default of `2`.  You probably don't need mroe nodes unless you have more than 20-25 students.

# Usage

**!Important** You must encrypt your group_vars/all/vault.yml before running your playbook.  You must add a vault_pass.txt to your home directory containing your password.

```
ansible-vault encrypt group_vars/all/vault.yml
```

You will be prompted to create a password and once complete, you can put this password is a file referenced in the ansible.cfg (vault_password_file = ~/.vault_pass.txt) file.  The current entry has a location of ~/.vault_pass.txt but you can chnage this at your discretion.

### Provision

Before you launch the provisioning script, copy the file `env.sh_example` to `env.sh`, and replace the placeholders with your AWS access key ID and secret access key.  Then, source that file, to place the variables into your environment.

```
source env.sh
AWS Keys exported
AWS_SECRET_ACCESS_KEY=01234567890abcdefghijlkmnopqrstuvwxyz!@#
AWS_ACCESS_KEY_ID=0123456789abcdefghij
```

```
ansible-playbook 1_provision.yml
ansible-playbook 2_load.yml
```

### Destroy

**[NOTE]:** This hidden directory contains the key pair for SSH access to instantiated host systems.

```
ansible-playbook 3_unregister.yml
```
