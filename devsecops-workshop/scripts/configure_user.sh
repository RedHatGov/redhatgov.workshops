#!/bin/bash

if ! $(oc whoami &>/dev/null); then
 printf "%s\n" "###############################################################################"
 printf "%s\n" "#  MAKE SURE YOU ARE LOGGED IN TO AN OPENSHIFT CLUSTER:                       #"
 printf "%s\n" "#  $ oc login https://your-openshift-cluster:8443                             #"
 printf "%s\n" "###############################################################################"
 exit 1
fi

username="$(oc whoami)"

oc new-project dev-$username   --display-name="Tasks - Dev"
oc new-project stage-$username --display-name="Tasks - Stage"
oc new-project cicd-$username --display-name="CI/CD"

oc policy add-role-to-user edit system:serviceaccount:cicd-$username:jenkins -n dev-$username
oc policy add-role-to-user edit system:serviceaccount:cicd-$username:jenkins -n stage-$username

oc new-app jenkins-ephemeral -n cicd-$username
