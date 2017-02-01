# OpenShift Terraform

Ansible playbook to install OpenShift using Terraform supported providers.

# Dependencies

## Terraform
Terraform needs to be [installed](https://www.terraform.io/intro/getting-started/install.html) locally.

### macOS

Install [Homebrew](http://brew.sh/) package manager.

```
brew install terraform
```

## Ansible

Ansible needs to be [installed](http://docs.ansible.com/ansible/intro_installation.html) locally.

### RHEL

```
yum install ansible
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
