# Quay and Clair Provisioner on OpenShift
This project will install Quay and Clair on Openshift.

## Must have existing OpenShift Environment
You can use either of the OpenShift provsioners from RedHatGov
 - https://github.com/RedHatGov/redhatgov.workshops/tree/master/openshift-aws-setup
 - https://github.com/RedHatGov/redhatgov.workshops/tree/master/openshift_terraform
 - https://github.com/gnunn1/openshift-aws-setup
 - https://github.com/jaredhocutt/openshift-provision
 - https://github.com/bit4man/ansible_agnostic_deployer

## Update Environment Variables for Quay and Clair Provisioner
Update the following variables for your environment in the provision-quay.sh

- hostname= Openshift Environment
- clusteradmin= Cluster Administrator
- clusteradminpass= Cluster Administrator
- domain= domain of your OpenShift Environment
- prefix= user prefix
- begin= first user #
- count= last user #
- ocuserpass= openshift password for users
- quayiouser= quay.io user with permission to pull quay container
- quayiopassword= quay.io password

## Run Quay and Clair Provisioner

This script will provision the Quay and Clair Pods along with their Databases.  

./provision-quay-batch.sh

## Manually Configure Quay

Unfortunately, there is no automated way to do this configuration in Quay.  

1.  Go to the Quay Enviroment you just provisioned.  It should take you to the Setup Wizard. .i.e http://quay-enterprise-quay-enterprise.apps.ocp-naps.redhatgov.io/

2.  Setup the DB.  Fill in the following values and Click Validate Database Settings

- Database Type: MySql
- Database Server: mysql
- Username: coreosuser
- Password: coreosuser
- Database Name: enterpriseregistrydb

3. Click Restart container.  Referesh the page after the container has restarted.

4. Enter Super User Info.  

5. Refresh page and login as the Super User.

6. Enter the Redis Information and Click Save Configuration Changes.  Configuration will be Validated and Click Save Configuration.

- Redis Hostname: quay-enterprise-redis
- Redis Port: 6379  

7. Click Restart container.  Referesh the page after the container has restarted.

8. Once restarted and refreshed, the installation should be complete.  Click View Superuser Panel

9. Click Registry Settings at the left menu.

10. Select "Enable Security Scanning" check mark

11. Enter Security Scanner Endpoint of your clairsvc: http://clairsvc:6060

12. Click Create Key

13. Select "Have the service provide a key" and click Start Approval.

If you are having issues with Clair, you may need to restart the clair container. Go to the clair pod logs and verify the following
- jwtproxy entered RUNNING state
- clair entered RUNNING state
- "finished fetching"..."rhel"

14. Save the configuration

15. Restart the Quay Container Manually

# Jenkins Node with Skopeo

This script also installs a Jenkins Slave Node with Skopeo.

In your pipeline, use "jenkins-slave-image-mgmt" for your jenkins slave node.
