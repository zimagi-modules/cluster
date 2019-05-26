from utility.cloud.aws import AWSServiceMixin
from .base import *


class AWSNetworkProvider(AWSServiceMixin, NetworkProvider):

    def provider_config(self, type = None):
        super().provider_config(type)
        self.option(str, 'region', 'us-east-1', help = 'AWS region name', config_name = 'aws_region')
        self.option(str, 'tenancy', 'default', help = 'AWS VPC instance tenancy (default | dedicated)', config_name = 'aws_vpc_tenancy')
        self.option(bool, 'dns_support', True, help = 'AWS VPC DNS support', config_name = 'aws_vpc_dns_support')
        self.option(bool, 'dns_hostnames', False, help = 'AWS VPC DNS hostname assignment', config_name = 'aws_vpc_dns_hostnames')

    def add_credentials(self, config):
        self.aws_credentials(config)

    def remove_credentials(self, config):
        self.clean_aws_credentials(config)


class AWSSubnetProvider(AWSServiceMixin, SubnetProvider):

    def provider_config(self, type = None):
        super().provider_config(type)
        self.option(str, 'zone', None, help = 'AWS availability zone (default random)', config_name = 'aws_zone')
        self.option(str, 'zone_suffix', None, help = 'AWS availability zone suffix (appended to region)', config_name = 'aws_zone_suffix')

    def add_credentials(self, config):
        self.aws_credentials(config)

    def remove_credentials(self, config):
        self.clean_aws_credentials(config)

    def initialize_terraform(self, instance, created):
        relations = self.command.get_relations(instance.facade)

        if instance.config['zone'] is None and instance.config['zone_suffix'] is not None:
            instance.config['zone'] = "{}{}".format(
                instance.network.config['region'],
                instance.config['zone_suffix']
            )
        super().initialize_terraform(instance, created)
        instance.config['nat_route_tables'] = self.get_nat_route_tables(relations['subnets'], instance.subnets)


class AWSFirewallProvider(AWSServiceMixin, FirewallProvider):

    def add_credentials(self, config):
        self.aws_credentials(config)

    def remove_credentials(self, config):
        self.clean_aws_credentials(config)

    def get_firewall_id(self):
        return self.instance.variables['security_group_id']


class AWSFirewallRuleProvider(AWSServiceMixin, FirewallRuleProvider):

    def add_credentials(self, config):
        self.aws_credentials(config)

    def remove_credentials(self, config):
        self.clean_aws_credentials(config)


class Provider(BaseProvider):

    def register_types(self):
        super().register_types()
        self.set('network', AWSNetworkProvider)
        self.set('subnet', AWSSubnetProvider)
        self.set('firewall', AWSFirewallProvider)
        self.set('firewall_rule', AWSFirewallRuleProvider)
