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

## Credits

Originally inspired by Ansible's [jboss-standalone][2] example project. Thanks!

[1]: http://jeremievallee.com/2016/07/27/aws-vpc-ansible/
[2]: https://github.com/ansible/ansible-examples/tree/master/jboss-standalone
