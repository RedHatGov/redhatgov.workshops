#!/bin/bash

hostname=
domain=
prefix=user
begin=1
count=1
clusteradmin=
clusteradminpass=
quayiouser=
quayiopassword=

for (( i = $begin; i <= $count; i++ )); do
 oc login "$hostname" --insecure-skip-tls-verify -u $prefix${i} -p "$prefix${i}"
 oc new-project 'quay-enterprise-'$prefix${i}'' --display-name="quay-enterprise"
done

oc login "$hostname" --insecure-skip-tls-verify -u "$clusteradmin" -p "$clusteradminpass"

for (( i = $begin; i <= $count; i++ )); do
  sed 's/namespace: quay-enterprise/namespace: quay-enterprise-'$prefix${i}'/' <quay-servicetoken-role-k8s1-6.yaml >quay-servicetoken-role-k8s1-6-batch.yaml
  oc create -f quay-servicetoken-role-k8s1-6-batch.yaml
  sed 's/namespace: quay-enterprise/namespace: quay-enterprise-'$prefix${i}'/' <quay-servicetoken-role-binding-k8s1-6.yaml >quay-servicetoken-role-binding-k8s1-6-batch.yaml
  oc create -f quay-servicetoken-role-binding-k8s1-6-batch.yaml
done

for (( i = $begin; i <= $count; i++ )); do
 oc login "$hostname" --insecure-skip-tls-verify -u $prefix${i} -p "$prefix${i}"
 oc project 'cicd-'$prefix${i}''
 oc process -f jenkins-slave-image-mgmt-template.yml | oc apply -f-
 #Install Quay
 oc project 'quay-enterprise-'$prefix${i}''
 sed 's/namespace: quay-enterprise/namespace: quay-enterprise-'$prefix${i}'/' <quay-enterprise-redis.yml >quay-enterprise-redis-batch.yml
 oc create -f quay-enterprise-redis-batch.yml
 oc new-app \
 -e DATABASE_SERVICE_NAME=mysql \
 -e MYSQL_USER=coreosuser \
 -e MYSQL_PASSWORD=coreosuser \
 -e MYSQL_DATABASE=enterpriseregistrydb \
 -e MYSQL_ROOT_PASSWORD=coreosuser \
 docker.io/mysql:5.7
 oc secrets new-dockercfg coreos-pull-secret --docker-server=quay.io --docker-username="$quayiouser"  --docker-password="$quayiopassword" --docker-email="$quayiouser"
 sed 's/namespace: quay-enterprise/namespace: quay-enterprise-'$prefix${i}'/' <quay-enterprise-config-secret.yml >quay-enterprise-config-secret-batch.yml
 oc create -f quay-enterprise-config-secret-batch.yml
 sed 's/namespace: quay-enterprise/namespace: quay-enterprise-'$prefix${i}'/' <quay-enterprise-app-rc.yml >quay-enterprise-app-rc-batch.yml
 oc create -f quay-enterprise-app-rc-batch.yml
 sed -e 's/namespace: quay-enterprise/namespace: quay-enterprise-'$prefix${i}'/' -e 's/name: quay-enterprise/name: quay-enterprise-'$prefix${i}'/' <quay-enterprise-service.yml >quay-enterprise-service-batch.yml
 oc create -f quay-enterprise-service-batch.yml
 oc expose svc quay-enterprise-"$prefix${i}"
 #Install Clair
 sed -e 's/<domain>/'$domain'/' -e 's/<user>/'$prefix${i}'/' <config-batch-template.yaml >config.yaml
 oc create secret generic clairsecret --from-file=./config.yaml
 oc create -f clair-kubernetes.yaml
 oc expose svc clairsvc
done
