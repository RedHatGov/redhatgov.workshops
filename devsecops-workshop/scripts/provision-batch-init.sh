#!/bin/bash

hostname=
password=
username=
begin=1
count=3
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
