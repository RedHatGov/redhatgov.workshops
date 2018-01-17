- Apply `atomic-openshift-excluder` to masters and nodes after installation
- AWS Atomic Host support
- Google Cloud Platform provider support
- Microsoft Azure provider support
- Document `-e @extra_vars.yml` file, for configurable variables
- Bootstrap any playbooks found in [openshift-ansible][1]
- Implement AWS dynamic route53 hosted zone id retrieval
- Implement [IDE on a container with Guacamole][2]
- Add ansible tower to project
- Delete intranet HostedZone (needs to be queried via bash)
- Release elastic IP address for EC2 instances upon master tear down
- Check is `AWS_SECRET_ACCESS_KEY` and `AWS_ACCESS_KEY_ID` are defined already
- [Setup VPC with public/private subnets][3]
- [Setup VPC with public/private subnets and Multi Availability Zones][3]

[1]: https://github.com/openshift/openshift-ansible
[2]: https://blog.openshift.com/put-ide-container-guacamole
[3]: http://jeremievallee.com/2016/07/27/aws-vpc-ansible/
