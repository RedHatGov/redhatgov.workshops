#!/bin/bash

export ANSIBLE_HOST_KEY_CHECKING=False

if [[ "$1" = "origin" ]]; then
 /usr/bin/ansible-playbook -i /home/{{ remote_user_name }}/openshift_inventory.cfg /home/{{ remote_user_name }}/openshift-ansible/playbooks/byo/config.yml
else
 /usr/bin/ansible-playbook -i /home/{{ remote_user_name }}/openshift_inventory.cfg /usr/share/ansible/openshift-ansible/playbooks/byo/config.yml
fi
