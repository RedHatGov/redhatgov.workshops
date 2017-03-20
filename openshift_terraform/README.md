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

### group_vars/all

```
default_domain: "${INSERT_VALUE_HERE}"
default_user: "${INSERT_VALUE_HERE}"
aws_access_key_id: "${INSERT_VALUE_HERE}"
aws_secret_access_key: "${INSERT_VALUE_HERE}"
```

### roles/terraform.infra.aws/defaults/main.yml

```
aws_route53_zone_id: "${INSERT_VALUE_HERE}"
```
The 'aws_route53_zone_id' value can be found using the following command:

```
aws route53 list-hosted-zones --query 'HostedZones[*]' --output text | \
    grep '\/hostedzone\/.*${default_domain_name}' | sed -e 's/.*\///' -e 's/[^a-zA-Z0-9].*//'
```

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

**!Important** These variables must be updated manually, based on `default_subdomain` value from `group_vars/all` file.

```
master.{{ default_subdomain }}
node.[0:1].{{ default_subdomain }}
```

**[NOTE]:** The value `[0:1]` is a [pattern](http://docs.ansible.com/ansible/intro_patterns.html#patterns) that declares how many OpenShift nodes to create. In this case it will create `node0` and `node1`.

# Usage

### Provision

```
ansible-playbook -i inventory site.yml
```

### Destroy

**[NOTE]:** This hidden directory contains the key pair for SSH access to instantiated host systems.

```
cd $(pwd)/.{{ default_domain }}
terraform destroy
```
