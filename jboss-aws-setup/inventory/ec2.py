#!/usr/bin/env python

'''
EC2 external inventory script
=================================

Generates inventory that Ansible can understand by making API request to
AWS EC2 using the Boto library.

NOTE: This script assumes Ansible is being executed where the environment
variables needed for Boto have already been set:
    export AWS_ACCESS_KEY_ID='AK123'
    export AWS_SECRET_ACCESS_KEY='abc123'

optional region environment variable if region is 'auto'

This script also assumes there is an ec2.ini file alongside it.  To specify a
different path to ec2.ini, define the EC2_INI_PATH environment variable:

    export EC2_INI_PATH=/path/to/my_ec2.ini

If you're using eucalyptus you need to set the above variables and
you need to define:

    export EC2_URL=http://hostname_of_your_cc:port/services/Eucalyptus

If you're using boto profiles (requires boto>=2.24.0) you can choose a profile
using the --boto-profile command line argument (e.g. ec2.py --boto-profile prod) or using
the AWS_PROFILE variable:

    AWS_PROFILE=prod ansible-playbook -i ec2.py myplaybook.yml

For more details, see: http://docs.pythonboto.org/en/latest/boto_config_tut.html

When run against a specific host, this script returns the following variables:
 - ec2_ami_launch_index
 - ec2_architecture
 - ec2_association
 - ec2_attachTime
 - ec2_attachment
 - ec2_attachmentId
 - ec2_block_devices
 - ec2_client_token
 - ec2_deleteOnTermination
 - ec2_description
 - ec2_deviceIndex
 - ec2_dns_name
 - ec2_eventsSet
 - ec2_group_name
 - ec2_hypervisor
 - ec2_id
 - ec2_image_id
 - ec2_instanceState
 - ec2_instance_type
 - ec2_ipOwnerId
 - ec2_ip_address
 - ec2_item
 - ec2_kernel
 - ec2_key_name
 - ec2_launch_time
 - ec2_monitored
 - ec2_monitoring
 - ec2_networkInterfaceId
 - ec2_ownerId
 - ec2_persistent
 - ec2_placement
 - ec2_platform
 - ec2_previous_state
 - ec2_private_dns_name
 - ec2_private_ip_address
 - ec2_publicIp
 - ec2_public_dns_name
 - ec2_ramdisk
 - ec2_reason
 - ec2_region
 - ec2_requester_id
 - ec2_root_device_name
 - ec2_root_device_type
 - ec2_security_group_ids
 - ec2_security_group_names
 - ec2_shutdown_state
 - ec2_sourceDestCheck
 - ec2_spot_instance_request_id
 - ec2_state
 - ec2_state_code
 - ec2_state_reason
 - ec2_status
 - ec2_subnet_id
 - ec2_tenancy
 - ec2_virtualization_type
 - ec2_vpc_id

These variables are pulled out of a boto.ec2.instance object. There is a lack of
consistency with variable spellings (camelCase and underscores) since this
just loops through all variables the object exposes. It is preferred to use the
ones with underscores when multiple exist.

In addition, if an instance has AWS Tags associated with it, each tag is a new
variable named:
 - ec2_tag_[Key] = [Value]

Security groups are comma-separated in 'ec2_security_group_ids' and
'ec2_security_group_names'.
'''

# (c) 2012, Peter Sankauskas
#
# This file is part of Ansible,
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

######################################################################

import sys
import os
import argparse
import re
from time import time
import boto
from boto import ec2
from boto import rds
from boto import elasticache
from boto import route53
from boto import sts
import six

from ansible.module_utils import ec2 as ec2_utils

HAS_BOTO3 = False
try:
    import boto3  # noqa
    HAS_BOTO3 = True
except ImportError:
    pass

from six.moves import configparser
from collections import defaultdict

try:
    import json
except ImportError:
    import simplejson as json

DEFAULTS = {
    'all_elasticache_clusters': 'False',
    'all_elasticache_nodes': 'False',
    'all_elasticache_replication_groups': 'False',
    'all_instances': 'False',
    'all_rds_instances': 'False',
    'aws_access_key_id': None,
    'aws_secret_access_key': None,
    'aws_security_token': None,
    'boto_profile': None,
    'cache_max_age': '300',
    'cache_path': '~/.ansible/tmp',
    'destination_variable': 'public_dns_name',
    'elasticache': 'True',
    'eucalyptus': 'False',
    'eucalyptus_host': None,
    'expand_csv_tags': 'False',
    'group_by_ami_id': 'True',
    'group_by_availability_zone': 'True',
    'group_by_aws_account': 'False',
    'group_by_elasticache_cluster': 'True',
    'group_by_elasticache_engine': 'True',
    'group_by_elasticache_parameter_group': 'True',
    'group_by_elasticache_replication_group': 'True',
    'group_by_instance_id': 'True',
    'group_by_instance_state': 'False',
    'group_by_instance_type': 'True',
    'group_by_key_pair': 'True',
    'group_by_platform': 'True',
    'group_by_rds_engine': 'True',
    'group_by_rds_parameter_group': 'True',
    'group_by_region': 'True',
    'group_by_route53_names': 'True',
    'group_by_security_group': 'True',
    'group_by_tag_keys': 'True',
    'group_by_tag_none': 'True',
    'group_by_vpc_id': 'True',
    'hostname_variable': None,
    'iam_role': None,
    'include_rds_clusters': 'False',
    'nested_groups': 'False',
    'pattern_exclude': None,
    'pattern_include': None,
    'rds': 'False',
    'regions': 'all',
    'regions_exclude': 'us-gov-west-1, cn-north-1',
    'replace_dash_in_groups': 'True',
    'route53': 'False',
    'route53_excluded_zones': '',
    'route53_hostnames': None,
    'stack_filters': 'False',
    'vpc_destination_variable': 'ip_address'
}


class Ec2Inventory(object):

    def _empty_inventory(self):
        return {"_meta": {"hostvars": {}}}

    def __init__(self):
        ''' Main execution path '''

        # Inventory grouped by instance IDs, tags, security groups, regions,
        # and availability zones
        self.inventory = self._empty_inventory()

        self.aws_account_id = None

        # Index of hostname (address) to instance ID
        self.index = {}

        # Boto profile to use (if any)
        self.boto_profile = None

        # AWS credentials.
        self.credentials = {}

        # Read settings and parse CLI arguments
        self.parse_cli_args()
        self.read_settings()

        # Make sure that profile_name is not passed at all if not set
        # as pre 2.24 boto will fall over otherwise
        if self.boto_profile:
            if not hasattr(boto.ec2.EC2Connection, 'profile_name'):
                self.fail_with_error("boto version must be >= 2.24 to use profile")

        # Cache
        if self.args.refresh_cache:
            self.do_api_calls_update_cache()
        elif not self.is_cache_valid():
            self.do_api_calls_update_cache()

        # Data to print
        if self.args.host:
            data_to_print = self.get_host_info()

        elif self.args.list:
            # Display list of instances for inventory
            if self.inventory == self._empty_inventory():
                data_to_print = self.get_inventory_from_cache()
            else:
                data_to_print = self.json_format_dict(self.inventory, True)

        print(data_to_print)

    def is_cache_valid(self):
        ''' Determines if the cache files have expired, or if it is still valid '''

        if os.path.isfile(self.cache_path_cache):
            mod_time = os.path.getmtime(self.cache_path_cache)
            current_time = time()
            if (mod_time + self.cache_max_age) > current_time:
                if os.path.isfile(self.cache_path_index):
                    return True

        return False

    def read_settings(self):
        ''' Reads the settings from the ec2.ini file '''

        scriptbasename = __file__
        scriptbasename = os.path.basename(scriptbasename)
        scriptbasename = scriptbasename.replace('.py', '')

        defaults = {
            'ec2': {
                'ini_fallback': os.path.join(os.path.dirname(__file__), 'ec2.ini'),
                'ini_path': os.path.join(os.path.dirname(__file__), '%s.ini' % scriptbasename)
            }
        }

        if six.PY3:
            config = configparser.ConfigParser(DEFAULTS)
        else:
            config = configparser.SafeConfigParser(DEFAULTS)
        ec2_ini_path = os.environ.get('EC2_INI_PATH', defaults['ec2']['ini_path'])
        ec2_ini_path = os.path.expanduser(os.path.expandvars(ec2_ini_path))

        if not os.path.isfile(ec2_ini_path):
            ec2_ini_path = os.path.expanduser(defaults['ec2']['ini_fallback'])

        if os.path.isfile(ec2_ini_path):
            config.read(ec2_ini_path)

        # Add empty sections if they don't exist
        try:
            config.add_section('ec2')
        except configparser.DuplicateSectionError:
            pass

        try:
            config.add_section('credentials')
        except configparser.DuplicateSectionError:
            pass

        # is eucalyptus?
        self.eucalyptus = config.getboolean('ec2', 'eucalyptus')
        self.eucalyptus_host = config.get('ec2', 'eucalyptus_host')

        # Regions
        self.regions = []
        configRegions = config.get('ec2', 'regions')
        if (configRegions == 'all'):
            if self.eucalyptus_host:
                self.regions.append(boto.connect_euca(host=self.eucalyptus_host).region.name, **self.credentials)
            else:
                configRegions_exclude = config.get('ec2', 'regions_exclude')

                for regionInfo in ec2.regions():
                    if regionInfo.name not in configRegions_exclude:
                        self.regions.append(regionInfo.name)
        else:
            self.regions = configRegions.split(",")
        if 'auto' in self.regions:
            env_region = os.environ.get('AWS_REGION')
            if env_region is None:
                env_region = os.environ.get('AWS_DEFAULT_REGION')
            self.regions = [env_region]

        # Destination addresses
        self.destination_variable = config.get('ec2', 'destination_variable')
        self.vpc_destination_variable = config.get('ec2', 'vpc_destination_variable')
        self.hostname_variable = config.get('ec2', 'hostname_variable')

        if config.has_option('ec2', 'destination_format') and \
           config.has_option('ec2', 'destination_format_tags'):
            self.destination_format = config.get('ec2', 'destination_format')
            self.destination_format_tags = config.get('ec2', 'destination_format_tags').split(',')
        else:
            self.destination_format = None
            self.destination_format_tags = None

        # Route53
        self.route53_enabled = config.getboolean('ec2', 'route53')
        self.route53_hostnames = config.get('ec2', 'route53_hostnames')

        self.route53_excluded_zones = []
        self.route53_excluded_zones = [a for a in config.get('ec2', 'route53_excluded_zones').split(',') if a]

        # Include RDS instances?
        self.rds_enabled = config.getboolean('ec2', 'rds')

        # Include RDS cluster instances?
        self.include_rds_clusters = config.getboolean('ec2', 'include_rds_clusters')

        # Include ElastiCache instances?
        self.elasticache_enabled = config.getboolean('ec2', 'elasticache')

        # Return all EC2 instances?
        self.all_instances = config.getboolean('ec2', 'all_instances')

        # Instance states to be gathered in inventory. Default is 'running'.
        # Setting 'all_instances' to 'yes' overrides this option.
        ec2_valid_instance_states = [
            'pending',
            'running',
            'shutting-down',
            'terminated',
            'stopping',
            'stopped'
        ]
        self.ec2_instance_states = []
        if self.all_instances:
            self.ec2_instance_states = ec2_valid_instance_states
        elif config.has_option('ec2', 'instance_states'):
            for instance_state in config.get('ec2', 'instance_states').split(','):
                instance_state = instance_state.strip()
                if instance_state not in ec2_valid_instance_states:
                    continue
                self.ec2_instance_states.append(instance_state)
        else:
            self.ec2_instance_states = ['running']

        # Return all RDS instances? (if RDS is enabled)
        self.all_rds_instances = config.getboolean('ec2', 'all_rds_instances')

        # Return all ElastiCache replication groups? (if ElastiCache is enabled)
        self.all_elasticache_replication_groups = config.getboolean('ec2', 'all_elasticache_replication_groups')

        # Return all ElastiCache clusters? (if ElastiCache is enabled)
        self.all_elasticache_clusters = config.getboolean('ec2', 'all_elasticache_clusters')

        # Return all ElastiCache nodes? (if ElastiCache is enabled)
        self.all_elasticache_nodes = config.getboolean('ec2', 'all_elasticache_nodes')

        # boto configuration profile (prefer CLI argument then environment variables then config file)
        self.boto_profile = self.args.boto_profile or \
            os.environ.get('AWS_PROFILE') or \
            config.get('ec2', 'boto_profile')

        # AWS credentials (prefer environment variables)
        if not (self.boto_profile or os.environ.get('AWS_ACCESS_KEY_ID') or
                os.environ.get('AWS_PROFILE')):

            aws_access_key_id = config.get('credentials', 'aws_access_key_id')
            aws_secret_access_key = config.get('credentials', 'aws_secret_access_key')
            aws_security_token = config.get('credentials', 'aws_security_token')

            if aws_access_key_id:
                self.credentials = {
                    'aws_access_key_id': aws_access_key_id,
                    'aws_secret_access_key': aws_secret_access_key
                }
                if aws_security_token:
                    self.credentials['security_token'] = aws_security_token

        # Cache related
        cache_dir = os.path.expanduser(config.get('ec2', 'cache_path'))
        if self.boto_profile:
            cache_dir = os.path.join(cache_dir, 'profile_' + self.boto_profile)
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

        cache_name = 'ansible-ec2'
        cache_id = self.boto_profile or os.environ.get('AWS_ACCESS_KEY_ID', self.credentials.get('aws_access_key_id'))
        if cache_id:
            cache_name = '%s-%s' % (cache_name, cache_id)
        self.cache_path_cache = os.path.join(cache_dir, "%s.cache" % cache_name)
        self.cache_path_index = os.path.join(cache_dir, "%s.index" % cache_name)
        self.cache_max_age = config.getint('ec2', 'cache_max_age')

        self.expand_csv_tags = config.getboolean('ec2', 'expand_csv_tags')

        # Configure nested groups instead of flat namespace.
        self.nested_groups = config.getboolean('ec2', 'nested_groups')

        # Replace dash or not in group names
        self.replace_dash_in_groups = config.getboolean('ec2', 'replace_dash_in_groups')

        # IAM role to assume for connection
        self.iam_role = config.get('ec2', 'iam_role')

        # Configure which groups should be created.

        group_by_options = [a for a in DEFAULTS if a.startswith('group_by')]
        for option in group_by_options:
            setattr(self, option, config.getboolean('ec2', option))

        # Do we need to just include hosts that match a pattern?
        self.pattern_include = config.get('ec2', 'pattern_include')
        if self.pattern_include:
            self.pattern_include = re.compile(self.pattern_include)

        # Do we need to exclude hosts that match a pattern?
        self.pattern_exclude = config.get('ec2', 'pattern_exclude')
        if self.pattern_exclude:
            self.pattern_exclude = re.compile(self.pattern_exclude)

        # Do we want to stack multiple filters?
        self.stack_filters = config.getboolean('ec2', 'stack_filters')

        # Instance filters (see boto and EC2 API docs). Ignore invalid filters.
        self.ec2_instance_filters = []

        if config.has_option('ec2', 'instance_filters'):
            filters = config.get('ec2', 'instance_filters')

            if self.stack_filters and '&' in filters:
                self.fail_with_error("AND filters along with stack_filter enabled is not supported.\n")

            filter_sets = [f for f in filters.split(',') if f]

            for filter_set in filter_sets:
                filters = {}
                filter_set = filter_set.strip()
                for instance_filter in filter_set.split("&"):
                    instance_filter = instance_filter.strip()
                    if not instance_filter or '=' not in instance_filter:
                        continue
                    filter_key, filter_value = [x.strip() for x in instance_filter.split('=', 1)]
                    if not filter_key:
                        continue
                    filters[filter_key] = filter_value
                self.ec2_instance_filters.append(filters.copy())

    def parse_cli_args(self):
        ''' Command line argument processing '''

        parser = argparse.ArgumentParser(description='Produce an Ansible Inventory file based on EC2')
        parser.add_argument('--list', action='store_true', default=True,
                            help='List instances (default: True)')
        parser.add_argument('--host', action='store',
                            help='Get all the variables about a specific instance')
        parser.add_argument('--refresh-cache', action='store_true', default=False,
                            help='Force refresh of cache by making API requests to EC2 (default: False - use cache files)')
        parser.add_argument('--profile', '--boto-profile', action='store', dest='boto_profile',
                            help='Use boto profile for connections to EC2')
        self.args = parser.parse_args()

    def do_api_calls_update_cache(self):
        ''' Do API calls to each region, and save data in cache files '''

        if self.route53_enabled:
            self.get_route53_records()

        for region in self.regions:
            self.get_instances_by_region(region)
            if self.rds_enabled:
                self.get_rds_instances_by_region(region)
            if self.elasticache_enabled:
                self.get_elasticache_clusters_by_region(region)
                self.get_elasticache_replication_groups_by_region(region)
            if self.include_rds_clusters:
                self.include_rds_clusters_by_region(region)

        self.write_to_cache(self.inventory, self.cache_path_cache)
        self.write_to_cache(self.index, self.cache_path_index)

    def connect(self, region):
        ''' create connection to api server'''
        if self.eucalyptus:
            conn = boto.connect_euca(host=self.eucalyptus_host, **self.credentials)
            conn.APIVersion = '2010-08-31'
        else:
            conn = self.connect_to_aws(ec2, region)
        return conn

    def boto_fix_security_token_in_profile(self, connect_args):
        ''' monkey patch for boto issue boto/boto#2100 '''
        profile = 'profile ' + self.boto_profile
        if boto.config.has_option(profile, 'aws_security_token'):
            connect_args['security_token'] = boto.config.get(profile, 'aws_security_token')
        return connect_args

    def connect_to_aws(self, module, region):
        connect_args = self.credentials

        # only pass the profile name if it's set (as it is not supported by older boto versions)
        if self.boto_profile:
            connect_args['profile_name'] = self.boto_profile
            self.boto_fix_security_token_in_profile(connect_args)

        if self.iam_role:
            sts_conn = sts.connect_to_region(region, **connect_args)
            role = sts_conn.assume_role(self.iam_role, 'ansible_dynamic_inventory')
            connect_args['aws_access_key_id'] = role.credentials.access_key
            connect_args['aws_secret_access_key'] = role.credentials.secret_key
            connect_args['security_token'] = role.credentials.session_token

        conn = module.connect_to_region(region, **connect_args)
        # connect_to_region will fail "silently" by returning None if the region name is wrong or not supported
        if conn is None:
            self.fail_with_error("region name: %s likely not supported, or AWS is down.  connection to region failed." % region)
        return conn

    def get_instances_by_region(self, region):
        ''' Makes an AWS EC2 API call to the list of instances in a particular
        region '''

        try:
            conn = self.connect(region)
            reservations = []
            if self.ec2_instance_filters:
                if self.stack_filters:
                    filters_dict = {}
                    for filters in self.ec2_instance_filters:
                        filters_dict.update(filters)
                    reservations.extend(conn.get_all_instances(filters=filters_dict))
                else:
                    for filters in self.ec2_instance_filters:
                        reservations.extend(conn.get_all_instances(filters=filters))
            else:
                reservations = conn.get_all_instances()

            # Pull the tags back in a second step
            # AWS are on record as saying that the tags fetched in the first `get_all_instances` request are not
            # reliable and may be missing, and the only way to guarantee they are there is by calling `get_all_tags`
            instance_ids = []
            for reservation in reservations:
                instance_ids.extend([instance.id for instance in reservation.instances])

            max_filter_value = 199
            tags = []
            for i in range(0, len(instance_ids), max_filter_value):
                tags.extend(conn.get_all_tags(filters={'resource-type': 'instance', 'resource-id': instance_ids[i:i + max_filter_value]}))

            tags_by_instance_id = defaultdict(dict)
            for tag in tags:
                tags_by_instance_id[tag.res_id][tag.name] = tag.value

            if (not self.aws_account_id) and reservations:
                self.aws_account_id = reservations[0].owner_id

            for reservation in reservations:
                for instance in reservation.instances:
                    instance.tags = tags_by_instance_id[instance.id]
                    self.add_instance(instance, region)

        except boto.exception.BotoServerError as e:
            if e.error_code == 'AuthFailure':
                error = self.get_auth_error_message()
            else:
                backend = 'Eucalyptus' if self.eucalyptus else 'AWS'
                error = "Error connecting to %s backend.\n%s" % (backend, e.message)
            self.fail_with_error(error, 'getting EC2 instances')

    def tags_match_filters(self, tags):
        ''' return True if given tags match configured filters '''
        if not self.ec2_instance_filters:
            return True

        for filters in self.ec2_instance_filters:
            for filter_name, filter_value in filters.items():
                if filter_name[:4] != 'tag:':
                    continue
                filter_name = filter_name[4:]
                if filter_name not in tags:
                    if self.stack_filters:
                        return False
                    continue
                if isinstance(filter_value, list):
                    if self.stack_filters and tags[filter_name] not in filter_value:
                        return False
                    if not self.stack_filters and tags[filter_name] in filter_value:
                        return True
                if isinstance(filter_value, six.string_types):
                    if self.stack_filters and tags[filter_name] != filter_value:
                        return False
                    if not self.stack_filters and tags[filter_name] == filter_value:
                        return True

        return self.stack_filters

    def get_rds_instances_by_region(self, region):
        ''' Makes an AWS API call to the list of RDS instances in a particular
        region '''

        if not HAS_BOTO3:
            self.fail_with_error("Working with RDS instances requires boto3 - please install boto3 and try again",
                                 "getting RDS instances")

        client = ec2_utils.boto3_inventory_conn('client', 'rds', region, **self.credentials)
        db_instances = client.describe_db_instances()

        try:
            conn = self.connect_to_aws(rds, region)
            if conn:
                marker = None
                while True:
                    instances = conn.get_all_dbinstances(marker=marker)
                    marker = instances.marker
                    for index, instance in enumerate(instances):
                        # Add tags to instances.
                        instance.arn = db_instances['DBInstances'][index]['DBInstanceArn']
                        tags = client.list_tags_for_resource(ResourceName=instance.arn)['TagList']
                        instance.tags = {}
                        for tag in tags:
                            instance.tags[tag['Key']] = tag['Value']
                        if self.tags_match_filters(instance.tags):
                            self.add_rds_instance(instance, region)
                    if not marker:
                        break
        except boto.exception.BotoServerError as e:
            error = e.reason

            if e.error_code == 'AuthFailure':
                error = self.get_auth_error_message()
            elif e.error_code == "OptInRequired":
                error = "RDS hasn't been enabled for this account yet. " \
                    "You must either log in to the RDS service through the AWS console to enable it, " \
                    "or set 'rds = False' in ec2.ini"
            elif not e.reason == "Forbidden":
                error = "Looks like AWS RDS is down:\n%s" % e.message
            self.fail_with_error(error, 'getting RDS instances')

    def include_rds_clusters_by_region(self, region):
        if not HAS_BOTO3:
            self.fail_with_error("Working with RDS clusters requires boto3 - please install boto3 and try again",
                                 "getting RDS clusters")

        client = ec2_utils.boto3_inventory_conn('client', 'rds', region, **self.credentials)

        marker, clusters = '', []
        while marker is not None:
            resp = client.describe_db_clusters(Marker=marker)
            clusters.extend(resp["DBClusters"])
            marker = resp.get('Marker', None)

        account_id = boto.connect_iam().get_user().arn.split(':')[4]
        c_dict = {}
        for c in clusters:
            # remove these datetime objects as there is no serialisation to json
            # currently in place and we don't need the data yet
            if 'EarliestRestorableTime' in c:
                del c['EarliestRestorableTime']
            if 'LatestRestorableTime' in c:
                del c['LatestRestorableTime']

            if not self.ec2_instance_filters:
                matches_filter = True
            else:
                matches_filter = False

            try:
                # arn:aws:rds:<region>:<account number>:<resourcetype>:<name>
                tags = client.list_tags_for_resource(
                    ResourceName='arn:aws:rds:' + region + ':' + account_id + ':cluster:' + c['DBClusterIdentifier'])
                c['Tags'] = tags['TagList']

                if self.ec2_instance_filters:
                    for filters in self.ec2_instance_filters:
                        for filter_key, filter_values in filters.items():
                            # get AWS tag key e.g. tag:env will be 'env'
                            tag_name = filter_key.split(":", 1)[1]
                            # Filter values is a list (if you put multiple values for the same tag name)
                            matches_filter = any(d['Key'] == tag_name and d['Value'] in filter_values for d in c['Tags'])

                            if matches_filter:
                                # it matches a filter, so stop looking for further matches
                                break

                        if matches_filter:
                            break

            except Exception as e:
                if e.message.find('DBInstanceNotFound') >= 0:
                    # AWS RDS bug (2016-01-06) means deletion does not fully complete and leave an 'empty' cluster.
                    # Ignore errors when trying to find tags for these
                    pass

            # ignore empty clusters caused by AWS bug
            if len(c['DBClusterMembers']) == 0:
                continue
            elif matches_filter:
                c_dict[c['DBClusterIdentifier']] = c

        self.inventory['db_clusters'] = c_dict

    def get_elasticache_clusters_by_region(self, region):
        ''' Makes an AWS API call to the list of ElastiCache clusters (with
        nodes' info) in a particular region.'''

        # ElastiCache boto module doesn't provide a get_all_instances method,
        # that's why we need to call describe directly (it would be called by
        # the shorthand method anyway...)
        try:
            conn = self.connect_to_aws(elasticache, region)
            if conn:
                # show_cache_node_info = True
                # because we also want nodes' information
                response = conn.describe_cache_clusters(None, None, None, True)

        except boto.exception.BotoServerError as e:
            error = e.reason

            if e.error_code == 'AuthFailure':
                error = self.get_auth_error_message()
            elif e.error_code == "OptInRequired":
                error = "ElastiCache hasn't been enabled for this account yet. " \
                    "You must either log in to the ElastiCache service through the AWS console to enable it, " \
                    "or set 'elasticache = False' in ec2.ini"
            elif not e.reason == "Forbidden":
                error = "Looks like AWS ElastiCache is down:\n%s" % e.message
            self.fail_with_error(error, 'getting ElastiCache clusters')

        try:
            # Boto also doesn't provide wrapper classes to CacheClusters or
            # CacheNodes. Because of that we can't make use of the get_list
            # method in the AWSQueryConnection. Let's do the work manually
            clusters = response['DescribeCacheClustersResponse']['DescribeCacheClustersResult']['CacheClusters']

        except KeyError as e:
            error = "ElastiCache query to AWS failed (unexpected format)."
            self.fail_with_error(error, 'getting ElastiCache clusters')

        for cluster in clusters:
            self.add_elasticache_cluster(cluster, region)

    def get_elasticache_replication_groups_by_region(self, region):
        ''' Makes an AWS API call to the list of ElastiCache replication groups
        in a particular region.'''

        # ElastiCache boto module doesn't provide a get_all_instances method,
        # that's why we need to call describe directly (it would be called by
        # the shorthand method anyway...)
        try:
            conn = self.connect_to_aws(elasticache, region)
            if conn:
                response = conn.describe_replication_groups()

        except boto.exception.BotoServerError as e:
            error = e.reason

            if e.error_code == 'AuthFailure'