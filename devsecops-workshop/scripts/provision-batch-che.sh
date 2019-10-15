#!/bin/bash

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
 DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
 SOURCE="$(readlink "$SOURCE")"
 [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
source "$DIR/provision-batch-init.sh"

check-hostname

# [TODO]
# oc adm policy add-cluster-role-to-user self-provisioner system:serviceaccount:eclipse-che:che

for (( i = $begin; i <= $count; i++ )); do
 oc login "$hostname" --insecure-skip-tls-verify -u "$username${i}" -p "$password${i}"
 oc process -f https://raw.githubusercontent.com/epe105/minishift-addons/master/add-ons/che/templates/che-single-user.yml \
  --param PROJECT_NAME=$CICD_NAMESPACE \
  --param DOMAIN_NAME=$HOSTNAME \
  --param OPENSHIFT_OAUTH_TOKEN="$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)" \
  | oc create -f -
 oc set resources dc/che --limits=cpu=1,memory=2Gi --requests=cpu=200m,memory=512Mi
 sleep "$pause"
done
