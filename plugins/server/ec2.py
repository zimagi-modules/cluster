from utility.cloud.aws import AWSServiceMixin
from .base import BaseProvider, SSHAccessError

import random


class Provider(AWSServiceMixin, BaseProvider):

    def provider_config(self, type = None):
        self.option(str, 'image', 'ami-0d2505740b82f7948', help = 'AWS image name', config_name = 'aws_ec2_image') # Ubuntu 18.04LTS hvm:ebs-ssd us-east-1
        self.option(str, 'machine', 't2.micro', help = 'AWS instance type', config_name = 'aws_ec2_type')
        self.option(str, 'tenancy', 'default', help = 'AWS instance tenancy (default | dedicated)', config_name = 'aws_ec2_tenancy')
        self.option(bool, 'monitoring', False, help = 'AWS monitoring enabled?', config_name = 'aws_ec2_monitoring')
        self.option(str, 'user', 'ubuntu', help = 'Server SSH user', config_name = 'aws_ec2_user')

        self.option(bool, 'ebs_optimized', False, help = 'AWS EBS obtimized server?', config_name = 'aws_ec2_ebs_optimized')
        self.option(str, 'ebs_type', 'gp2', help = 'AWS data drive EBS type', config_name = 'aws_ec2_ebs_type')
        self.option(int, 'ebs_size', 10, help = 'AWS data drive EBS volume size (GB)', config_name = 'aws_ec2_ebs_size')
        self.option(int, 'ebs_iops', None, help = 'AWS data drive EBS provisioned IOPS', config_name = 'aws_ec2_ebs_size')

    def add_credentials(self, config):
        self.aws_credentials(config)

    def remove_credentials(self, config):
        self.clean_aws_credentials(config)

    def initialize_terraform(self, instance, created):
        relations = self.command.get_relations(instance.facade)

        if 'key_name' not in instance.config:
            self.ec2_conn = self.ec2(instance.subnet.network)
            key_name, private_key = self._create_keypair(self.ec2_conn)

            instance.config['key_name'] = key_name
            instance.private_key = private_key

        super().initialize_terraform(instance, created)
        instance.config['use_public_ip'] = instance.subnet.use_public_ip
        instance.config['security_groups'] = self.get_security_groups(relations['firewalls'], instance.firewalls)

    def prepare_instance(self, instance, created):
        if instance.variables.get('public_ip_address', None):
            instance.public_ip = instance.variables['public_ip_address']

        instance.private_ip = instance.variables['private_ip_address']
        super().prepare_instance(instance, created)


    def finalize_terraform(self, instance):
        super().finalize_terraform(instance)
        self.ec2_conn = self.ec2(instance.subnet.network)
        self._delete_keypair(self.ec2_conn, instance.config['key_name'])


    def _get_keynames(self, ec2):
        key_names = []
        keypairs = ec2.describe_key_pairs()
        for keypair in keypairs['KeyPairs']:
            key_names.append(keypair['KeyName'])

        return key_names

    def _create_keypair(self, ec2):
        key_names = self._get_keynames(ec2)

        while True:
            key_name = "ce_{}".format(random.randint(1, 1000001))
            if key_name not in key_names:
                break

        keypair = ec2.create_key_pair(KeyName = key_name)
        return (key_name, keypair['KeyMaterial'])

    def _delete_keypair(self, ec2, key_name):
        return ec2.delete_key_pair(KeyName = key_name)
