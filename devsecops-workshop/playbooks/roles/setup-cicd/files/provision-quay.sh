#!/bin/bash

hostname=https://{{ openshift_public_hostname }}
clusteradmin={{ clusteradmin }}
clusteradminpass={{ clusteradminpass }}
domain=apps.{{ openshift_public_hostname }}
username={{ generic_user }}
prefix={{ generic_user }}
begin={{ generic_count_begin }}
count={{ generic_count }}
ocuserpass={{ generic_pass }}
password={{ generic_pass }}
quayiouser={{ quayiouser }}
quayiopassword={{ quayiopassword }}

# Logout of any user
oc logout

# Login as cluster admin
oc login "$hostname" --insecure-skip-tls-verify -u "$clusteradmin" -p "$clusteradminpass"

# Import Images
oc project openshift
oc import-image jenkins:2

# Check if quay-enterprise project already exists
if ! oc get project quay-enterprise &>/dev/null; then
 oc new-project quay-enterprise
 oc create -f quay-servicetoken-role-k8s1-6.yaml
 oc create -f quay-servicetoken-role-binding-k8s1-6.yaml
 oc adm policy add-scc-to-user anyuid -z default

 # Install Quay
 oc project quay-enterprise
 oc create -f quay-enterprise-redis.yml
 oc new-app \
  -e DATABASE_SERVICE_NAME=mysql \
  -e MYSQL_USER=coreosuser \
  -e MYSQL_PASSWORD=coreosuser \
  -e MYSQL_DATABASE=enterpriseregistrydb \
  -e MYSQL_ROOT_PASSWORD=coreosuser \
  docker.io/mysql:5.7
 oc secrets new-dockercfg coreos-pull-secret --docker-server=quay.io --docker-username="$quayiouser"  --docker-password="$quayiopassword" --docker-email="$quayiouser"
 oc create -f quay-enterprise-config-secret.yml
 oc create -f quay-enterprise-app-rc.yml
 oc create -f quay-enterprise-service.yml
 oc expose svc quay-enterprise

 # Install Clair
 sed 's/<domain>/'$domain'/' <config-template.yaml >config.yaml
 oc create secret generic clairsecret --from-file=./config.yaml
 oc create -f clair-kubernetes.yaml
 oc expose svc clairsvc
fi

# Install Skopeo on Jenkins
for (( i = $begin; i <= $count; i++ )); do
 oc login "$hostname" --insecure-skip-tls-verify -u "$username${i}" -p "$password"
 oc project "cicd-$prefix${i}"
 oc process -f jenkins-slave-image-mgmt-template.yml | oc apply -f-
done
