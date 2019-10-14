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

for (( i = $begin; i <= $count; i++ )); do
 oc login "$hostname" --insecure-skip-tls-verify -u "$username${i}" -p "$password"
 ./provision.sh deploy --deploy-che --ephemeral
 sleep "$pause"

 # Patch service account token for Che
 CHE_TOKEN="$(oc sa get-token che -n cicd-$username${i})"
 JSON_STRING='{"data":{"openshift-oauth-token":"'"$CHE_TOKEN"'"}}'
 oc patch configmaps che -p $JSON_STRING -n cicd-$username${i}
 JSON_STRING='{"data":{"pvc-strategy":"common"}}'
 oc patch configmaps che -p $JSON_STRING -n cicd-$username${i}
 oc rollout latest dc/che -n cicd-$username${i}
done
