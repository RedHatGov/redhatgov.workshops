#!/bin/bash

hostname=
clusteradmin=
clusteradminpass=

oc login "$hostname" --insecure-skip-tls-verify -u "$clusteradmin" -p "$clusteradminpass"

oc project quay-enterprise

# Delete Quay
oc delete service quay
oc delete deploymentconfigs quay
oc delete route quay
oc delete imagestreams quay
oc delete buildconfig quay


oc delete route quay-enterprise
oc delete service quay-enterprise

oc delete service quay-enterprise-app
oc delete route quay-enterprise-app
oc delete imagestreams quay-enterprise-app
oc delete buildconfig quay-enterprise-app
oc delete deployments quay-enterprise-app
oc delete secret coreos-pull-secret

# Delete Mysql
oc delete service mysql
oc delete deploymentconfigs mysql
oc delete route mysql
oc delete imagestreams mysql
oc delete buildconfig mysql

# Delete Quay password
