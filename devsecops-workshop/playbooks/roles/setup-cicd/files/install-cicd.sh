#!/usr/bin/env bash

export ANSIBLE_HOST_KEY_CHECKING=False

ansible-playbook -v /home/{{ ansible_user }}/cache_docker_images.yml

if [ {{ install_cicd_projects }} == True ]; then
    pushd /home/{{ ansible_user }}/devsecops-workshop/scripts &>/dev/null
    ./provision-batch-setup.sh
    popd &>/dev/null;
fi

if [ {{ install_quay }} == True ]; then
    pushd /home/{{ ansible_user }}/devsecops-workshop/scripts/quay &>/dev/null
    ./provision-quay.sh
    popd &>/dev/null;
fi