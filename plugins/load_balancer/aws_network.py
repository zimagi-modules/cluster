from utility.cloud.aws import AWSServiceMixin
from .base import *


class AWSNetworkLoadBalancerProvider(AWSServiceMixin, LoadBalancerProvider):

    def add_credentials(self, config):
        self.aws_credentials(config)

    def remove_credentials(self, config):
        self.clean_aws_credentials(config)

    def initialize_terraform(self, instance, created):
        relations = self.command.get_relations(instance.facade)
        super().initialize_terraform(instance, created)

        instance.config['subnets'] = self.get_subnets(instance.network)
        instance.config['security_groups'] = self.get_security_groups(relations['firewalls'], instance.firewalls)


class AWSNetworkLoadBalancerListenerProvider(AWSServiceMixin, LoadBalancerListenerProvider):

    def add_credentials(self, config):
        self.aws_credentials(config)

    def remove_credentials(self, config):
        self.clean_aws_credentials(config)


class Provider(BaseProvider):

    def register_types(self):
        super().register_types()
        self.set('load_balancer', AWSNetworkLoadBalancerProvider)
        self.set('load_balancer_listener', AWSNetworkLoadBalancerListenerProvider)
