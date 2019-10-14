#!/usr/bin/env bash

export ANSIBLE_HOST_KEY_CHECKING=False

ansible-playbook -v /home/{{ ansible_user }}/cache_docker_images.yml
