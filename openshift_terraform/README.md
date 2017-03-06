# OpenShift Terraform

Ansible playbook to install OpenShift using Terraform supported providers.

# Dependencies

- [Terraform](https://www.terraform.io/intro/getting-started/install.html) (v0.8.5)
- [Ansible](http://docs.ansible.com/ansible/intro_installation.html) (v2.2.1.0)
- [AWS Command Line Interface](http://docs.aws.amazon.com/cli/latest/userguide/installing.html)
- [Red Hat Customer Portal Activation Key](https://access.redhat.com/articles/1378093)

# Required

The following settings must be set before usage.

### group_vars/all

```
default_domain: "${INSERT_VALUE_HERE}"
default_subdomain: "${INSERT_VALUE_HERE}.{{ default_domain }}"
default_wildcard: "${INSERT_VALUE_HERE}.{{ default_subdomain }}"
default_user: "${INSERT_VALUE_HERE}"
aws_access_key_id: "${INSERT_VALUE_HERE}"
aws_secret_access_key: "${INSERT_VALUE_HERE}"
```

### roles/terraform.infra.aws/defaults/main.yml

```
aws_route53_zone_id: "${INSERT_VALUE_HERE}"
```

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

**[IMPORTANT]:** These variables must be updated manually, based on `default_subdomain` value from `group_vars/all` section above.

```
master.{{ default_subdomain }}
node.[0:1].{{ default_subdomain }}
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
