# OpenShift Terraform

This Ansible playbook is used to install OpenShift on Terraform supported providers.  Out of the box this playbook will create a three node OpenShift cluster with a Master and two OpenShift nodes on Amazon EC2 instances in the AWS cloud.  Future versions of this playbook will enable more providers.  This playbook can be modified to increase the number of nodes in the cluster if so desired.

After checking out this repository, search for the string "INSERT_VALUES_HERE" through out the files and replace that string with the appropriate values for the field.  The files and fields that need this change are listed below.

# Dependencies

- [Terraform](https://www.terraform.io/intro/getting-started/install.html) (v0.8.5)
- [Ansible](http://docs.ansible.com/ansible/intro_installation.html) (v2.2.1.0)
- [AWS Command Line Interface](http://docs.aws.amazon.com/cli/latest/userguide/installing.html)
- [Red Hat Customer Portal Activation Key](https://access.redhat.com/articles/1378093)

# Required

The following settings must be set before usage.

### group_vars/all

```
default_domain_name: "${INSERT_VALUE_HERE}"
default_user: "${INSERT_VALUE_HERE}"
aws_access_key_id: "${INSERT_VALUE_HERE}"
aws_secret_access_key: "${INSERT_VALUE_HERE}"
```

### roles/terraform.infra.aws/defaults/main.yml

```
aws_route53_zone_id: "${INSERT_VALUE_HERE}"
```
The 'aws_route53_zone_id' value can be found using the following command:

aws route53 list-hosted-zones --query 'HostedZones[*]' --output text |
grep '\/hostedzone\/.*${default_domain_name}' | sed -e 's/.*\///' -e
's/[^a-zA-Z0-9].*//'

Make sure to replace "${default_domain_name}" with the domain you've purchased through AWS and managed by Route53.


### roles/openshift.prereq/defaults/main.yml

```
rhel_rhsm_activationkey: "${INSERT_VALUE_HERE}"
rhel_rhsm_org_id: "${INSERT_VALUE_HERE}"
```

### roles/openshift.config/defaults/main.yml

```
openshift_cluster_admin_username: "${INSERT_VALUE_HERE}"
openshift_cluster_admin_password: "${INSERT_VALUE_HERE}"
```

### inventory

The value '[0:1]' tells ansible how many OpenShift nodes to create.  In this case it will create node0 and node1.
  I
```
master.ose.${INSERT_VALUE_HERE}
node.[0:1].ose.${INSERT_VALUE_HERE}
```

# Usage

## Provision

```
ansible-playbook -i inventory site.yml
```

## Destroy the cluster & provider resources

```
cd $(pwd)/.terraform
terraform destroy
```
