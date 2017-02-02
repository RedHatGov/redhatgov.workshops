#cloud-config
users:
- default

system_info:
  default_user:
    name: {{ ec2_default_user }}
