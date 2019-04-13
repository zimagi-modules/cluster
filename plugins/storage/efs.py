from utility.cloud.aws import AWSServiceMixin
from .base import *


class EFSStorageProvider(AWSServiceMixin, StorageProvider):

    def provider_config(self, type = None):
        self.option(str, 'performance_mode', 'generalPurpose', help = 'AWS EFS performance mode (can also be: maxIO)', config_name = 'aws_efs_perf_mode')
        self.option(str, 'throughput_mode', 'bursting', help = 'AWS EFS throughput mode (can also be: provisioned)', config_name = 'aws_efs_tp_mode')
        self.option(int, 'provisioned_throughput', None, help = 'AWS EFS throughput in MiB/s', config_name = 'aws_efs_prov_tp')
        self.option(bool, 'encrypted', False, help = 'AWS EFS encrypted filesystem?', config_name = 'aws_efs_encrypted')

    def add_credentials(self, config):
        self.aws_credentials(config)

    def remove_credentials(self, config):
        self.clean_aws_credentials(config)


class EFSStorageMountProvider(AWSServiceMixin, StorageMountProvider):

    def add_credentials(self, config):
        self.aws_credentials(config)

    def remove_credentials(self, config):
        self.clean_aws_credentials(config)

    def initialize_terraform(self, instance, created):
        relations = self.command.get_relations(instance.facade)
        super().initialize_terraform(instance, created)
        instance.config['security_groups'] = self.get_security_groups(relations['firewalls'], instance.firewalls)

    def prepare_instance(self, instance, created):
        instance.remote_path = '/'
        instance.remote_host = instance.variables['mount_ip']
        super().prepare_instance(instance, created)


class Provider(BaseProvider):

    def register_types(self):
        super().register_types()
        self.set('storage', EFSStorageProvider)
        self.set('mount', EFSStorageMountProvider)
