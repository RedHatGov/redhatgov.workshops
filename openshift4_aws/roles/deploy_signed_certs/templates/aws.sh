#!/usr/bin/env bash

ACME_VERSION={{ acme_version }}

# Get apps wildcard domain.
LE_WILDCARD=$(oc get ingresscontroller default -n openshift-ingress-operator -o jsonpath='{.status.domain}')
echo "LE_WILDCARD: $LE_WILDCARD"

# From wildcard domain, determine the api url.
LE_API=$( echo "$LE_WILDCARD" | cut -d'.' -f2- )
LE_API="api.$LE_API"
echo "API: $LE_API"

issue_args=(
    --issue
    --dns dns_aws
    -d "$LE_API"
    -d "*.$LE_WILDCARD"
    --home /tmp
    --cert-home /tmp
    --config-home /tmp
    --debug
)
if [ "$STAGING" == true ] ; then
    issue_args+=(--staging)
fi

# Issue certs.
echo "Run: ./acme.sh ${issue_args[@]}"
./acme.sh "${issue_args[@]}"

install_args=(
    --install-cert
    -d "$LE_API"
    -d "*.$LE_WILDCARD"
    --cert-file "$FINAL_CERTS/cert.pem"
    --key-file "$FINAL_CERTS/key.pem"
    --fullchain-file "$FINAL_CERTS/fullchain.pem"
    --ca-file "$FINAL_CERTS/ca.cer"
    --home /tmp
    --cert-home /tmp
    --config-home /tmp
    --debug
)
if [ "$STAGING" == true ] ; then
    install_args+=(--staging)
fi

# Run install.
echo "Run: ./acme.sh ${install_args[@]}"
./acme.sh "${install_args[@]}"

# Lets Enctrypt cert secret name.
LE_CERTS_SECRET_NAME="le-certs-$(date '+%Y-%m-%d')"

if [ -f "$FINAL_CERTS/fullchain.pem" ]; then
    secret_args=(
        create
        secret
        tls
        "$LE_CERTS_SECRET_NAME"
        --cert="$FINAL_CERTS/fullchain.pem"
        --key="$FINAL_CERTS/key.pem"
    )
    if [ "$STAGING" == true ] ; then
        secret_args+=(--dry-run=true)
        secret_args+=(-o yaml)
    fi

    # Create tls secret.  Only dry-run and ouptut yaml if STAGING.
    oc "${secret_args[@]}" -n openshift-ingress
    oc "${secret_args[@]}" -n openshift-config

    # Patch ingress with new secret if NOT STAGING.
    if [ "$STAGING" == false ] ; then
        oc patch ingresscontroller default -n openshift-ingress-operator --type=merge --patch='{"spec": { "defaultCertificate": { "name": "'$LE_CERTS_SECRET_NAME'" }}}'
        # Patch api server with new secret if NOT STAGING.
        if [ "$PATCH_API_SERVER" == true ] ; then
            oc patch apiserver cluster --type=merge -p '{"spec":{"servingCerts": {"namedCertificates": [{"names": ["'$LE_API'"], "servingCertificate": {"name": "'$LE_CERTS_SECRET_NAME'"}}]}}}'
        fi
    fi

else
    echo "Error generating certs.  Please see logs."
fi