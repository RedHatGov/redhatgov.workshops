#!/bin/bash

host=$( grep -A1 '\[admin_rhel_node\]' inventory/hosts | tail -1 | sed 's/ .*//' )
ip=$( grep -A1 '\[admin_rhel_node\]' inventory/hosts | tail -1 | sed 's/.*ansible_ssh_host=//' )
workshop=$( echo $host | awk -F\. '{ print $1 }' )

echo "Logging into $host..."

ssh -i .redhatgov/${workshop}-key ec2-user@${ip}

