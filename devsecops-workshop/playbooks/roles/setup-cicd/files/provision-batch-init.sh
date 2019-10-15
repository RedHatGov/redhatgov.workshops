#!/bin/bash

hostname=https://{{ openshift_public_hostname }}
password={{ generic_pass }}
username={{ generic_user }}
begin={{ generic_count_begin }}
count={{ generic_count }}
pause=5

function check-hostname() {
 if [[ -z "$hostname" ]]; then
  printf "%s\n" "###############################################################################"
  printf "%s\n" "#  MAKE SURE YOU ARE LOGGED IN TO AN OPENSHIFT CLUSTER:                       #"
  printf "%s\n" "#  $ oc login https://your-openshift-cluster:8443                             #"
  printf "%s\n" "###############################################################################"
  exit 1
 fi
}
