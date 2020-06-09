from systems.plugins.index import BaseProvider
from .base import SSHAccessError

import random


class Provider(BaseProvider('server', 'ec2')):

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
