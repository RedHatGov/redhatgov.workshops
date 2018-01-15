### Install

#### GNU/Linux, or macOS

```sh
#!/bin/bash

git clone https://github.com/ecwpz91/jboss-aws-setup
cd jboss-aws-setup
```

##### No `git`? No problem!

```sh
#!/bin/bash

DIRPATH="${HOME}/Downloads/jboss-aws-setup"; GITUSER="ecwpz91"
GITREPO="https://github.com/${GITUSER}/jboss-aws-setup/archive/master.zip"
ARCHIVE="$(printf "%s" "${GITREPO##*/}")"

# Download and extract
wget $GITREPO \
&& temp="$(mktemp -d)" \
&& unzip -d $temp $ARCHIVE \
&& mkdir -p $DIRPATH \
&& mv $temp/*/* $DIRPATH \
&& rm -rf $temp $ARCHIVE \
&& cd $DIRPATH \
&& unset DIRPATH GITUSER GITREPO ARCHIVE temp
```

## Provisioning Amazon Web Services

The playbook `aws-jboss-eap-playbook.yml` may be used to provision hosts in preparation for running this JBoss deployment example.

```sh
source setup.sh.example
openshift-aws-setup playbooks/aws-jboss-eap-playbook.yml
```
## JBoss EAP Application Deployment

The playbook `aws-deploy-application.yml` may be used to deploy the HelloWorld demo application to JBoss hosts that have been deployed using `aws-jboss-eap-playbook.yml`, as above.

Run the playbook using:

```sh
source setup.sh.example
openshift-aws-setup playbooks/aws-deploy-application.yml
```

The HelloWorld application will be available at `http://<jboss server>:<http_port>/helloworld`

The Ticket Monster application will be available at `http://<jboss server>:<http_port>/ticket-monster`

### Ideas for Improvement

Here are some ideas for ways that these playbooks could be extended:

- Write a playbook or an Ansible module to configure JBoss users.
- Extend this configuration to multiple application servers fronted by a load
balancer or other web server frontend.
- Implement AWS provisioned environment tear-down.
- Implement Google Cloud Platform provider support.
- Implement Microsoft Azure provider support.
- Implement AWS dynamic route53 hosted zone id retrieval.
- Implement [vpc with public/private subnets][1].
- Implement [vpc with public/private subnets and Multi Availability Zones][1].
- Implement `vault_password_file` setup via `passlib-hash()` from `hack/lib/util.sh`.

Would love to see contributions and improvements, so please fork this repo on
GitHub and send your changes via pull request(s).

## Credits

Originally inspired by Ansible's [jboss-standalone][2] example project. Thanks!

[1]: http://jeremievallee.com/2016/07/27/aws-vpc-ansible/
[2]: https://github.com/ansible/ansible-examples/tree/master/jboss-standalone
