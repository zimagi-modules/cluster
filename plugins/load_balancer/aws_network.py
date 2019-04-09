from utility.cloud.aws import AWSServiceMixin
from .base import *


class AWSNetworkLoadBalancerProvider(AWSServiceMixin, LoadBalancerProvider):

    def initialize_terraform(self, instance, created):
        relations = self.command.get_relations(instance.facade)

        self.aws_credentials(instance.config)
        super().initialize_terraform(instance, created)

        instance.config['subnets'] = self.get_subnets(instance.network)
        instance.config['security_groups'] = self.get_security_groups(relations['firewalls'], instance.firewalls)

    def prepare_instance(self, instance, created):
        super().prepare_instance(instance, created)
        self.clean_aws_credentials(instance.config)

    def finalize_terraform(self, instance):
        self.aws_credentials(instance.config)
        super().finalize_terraform(instance)


class AWSNetworkLoadBalancerListenerProvider(AWSServiceMixin, LoadBalancerListenerProvider):

    def initialize_terraform(self, instance, created):
        self.aws_credentials(instance.config)
        super().initialize_terraform(instance, created)

    def prepare_instance(self, instance, created):
        super().prepare_instance(instance, created)
        self.clean_aws_credentials(instance.config)

    def finalize_terraform(self, instance):
        self.aws_credentials(instance.config)
        super().finalize_terraform(instance)


class Provider(BaseProvider):

    def register_types(self):
        super().register_types()
        self.set('load_balancer', AWSNetworkLoadBalancerProvider)
        self.set('load_balancer_listener', AWSNetworkLoadBalancerListenerProvider)
