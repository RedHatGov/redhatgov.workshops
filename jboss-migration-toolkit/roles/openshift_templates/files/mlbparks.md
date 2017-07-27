# MLB Parks

# oc cluster up \                                                                
#   --host-pv-dir=/data \
#   --host-data-dir=/data \
#   --metrics=true \
#   --logging=true \
#   --image=registry.access.redhat.com/openshift3/ose


oc whoami

oc login -u system:admin

oc login -u developer

oc status
oc project

oc new-project mlbparks --description="MLB Parks WildFly & MongoDB Demo" --display-name="MLB Parks"

# Template


oc create -f mlbparks-template-wildfly.json 

# Launch App

launch app via web

or

oc new-app mlbparks-wildfly

oc new-app mlbparks-eap

-----Logs

oc logs -f bc/mlbparks

oc status

oc delete project mlbparks
