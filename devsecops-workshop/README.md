# Prerequisites

We recommend that you provision about 5-10GBs of Memory per User.  For a workshop of 20 people, we recommend 4-6 m4.xlarge app nodes or larger.

 - Modern HTML5 Standard Compliant Web Browser
 - A recent stable version of Python 2.7 and the latest stable version of the boto libraries (lxml, pip, boto, boto3, and botocore)
 - The latest stable versions of Ansible.
 - An AWS account with the aws cli setup to use your access key
 - For best performance, ensure that the version of the oc cli you use matches the version of the OpenShift cluster. With matching versions users' lab content can and should provision in ~15-30 seconds. 

## Must have existing OpenShift Environment
You can use either of the OpenShift provsioners from RedHatGov
 - https://github.com/RedHatGov/redhatgov.workshops/tree/master/openshift-aws-setup
 - https://github.com/RedHatGov/redhatgov.workshops/tree/master/openshift_terraform
 - https://github.com/gnunn1/openshift-aws-setup
 - https://github.com/jaredhocutt/openshift-provision
 - https://github.com/bit4man/ansible_agnostic_deployer

Your workshop users in your OpenShift Environment should have the same password.

# Environment Setup
If you'd like to setup an individual environment, use the commands below to set it up or delete the single environment.

## Ansible Playbook for setting up the Entire Workshop Enviornment on OpenShift
- copy over you ssh key into the /keys folder and set the permission to 400
- the Update your configuration aws.example.env and aws.example.yml in the vars/ folder
- run the ansible playbook using the devsecops-playbook-run.sh script
- manually restart your OpenShift Environment after the playbook run
$ ./devsecops-playbook-run.sh script

## Help

$ scripts/provision.sh --help

### Individual Environment

$ scripts/provision.sh deploy --deploy-che --ephemeral

### Individual Delete

$ scripts/provision.sh delete

## Batch Setup
If you'd like to setup the workshop for numerous users, go into the provision-batch-setup.sh script and update for loop with the amount of users .  This will create an isolated environment per user.

To run the script

$ ./provision-batch-setup.sh

## Batch Delete
If you'd like to delete, run the script for the users you'd like to delete by updating the for loop

To run the script

$ ./provision-batch-delete.sh

# Quay and Clair Provisioner on OpenShift
Note: If the ansible playbook was run, skip to "Manually Configure Quay" Section.

This project will install Quay and Clair on Openshift.

## Must have existing OpenShift Environment with a Valid Certificate
Please make sure you have a Valid Certificate and not a self signed certificate.

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

2.  Setup the DB.  Fill in the following values and Click Validate Database Settings.  This could take several minutes, and you may need to refresh your page.

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

10. Scroll down and Select "Enable Security Scanning" check mark

11. Enter Security Scanner Endpoint of your clairsvc: http://clairsvc:6060

12. Click Create Key

13. Select "Have the service provide a key" and click Start Approval.

- If Clair is not being responsive with providing a service key, restart Clair and try again.

14. Save the configuration

15. Restart the Quay Container Manually

If you are having issues with Clair, you may need to restart the clair container. Go to the clair pod logs and verify the following
- jwtproxy entered RUNNING state
- clair entered RUNNING state
- "finished fetching"..."rhel"

## Jenkins Node with Skopeo

This script also installs a Jenkins Slave Node with Skopeo.

In your pipeline, use "jenkins-slave-image-mgmt" for your jenkins slave node.

# Creating Workshop WebPage

Please update the following values in your vars/aws.example.yml for creating a Environment Workshop WebPage.

-  value must be unique.  The prefix for the subdomain used for workshop page creation.  Please use a separate subdomain from your openshift environment to avoid conflicts. Your webpage will be: subdomain.domain.com
    -  ec2_name_prefix: 
    - i.e aiworkshop      
