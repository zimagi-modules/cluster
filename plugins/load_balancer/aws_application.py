from utility.cloud.aws import AWSServiceMixin
from .base import *


class AWSApplicationLoadBalancerProvider(AWSServiceMixin, LoadBalancerProvider):

    def provider_config(self, type = None):
        self.option(int, 'idle_timeout', 60, help = 'Idle timeout (secs)')

    def initialize_terraform(self, instance, created):
        relations = self.command.get_relations(instance.facade)

        self.aws_credentials(instance.config)
        super().initialize_terraform(instance, created)

        instance.config['subnets'] = self.get_subnets(instance.network)
        instance.config['security_groups'] = self.get_security_groups(relations['firewalls'])

    def prepare_instance(self, instance, created):
        super().prepare_instance(instance, created)
        self.clean_aws_credentials(instance.config)

    def finalize_terraform(self, instance):
        self.aws_credentials(instance.config)
        super().finalize_terraform(instance)


class AWSApplicationLoadBalancerListenerProvider(AWSServiceMixin, LoadBalancerListenerProvider):

    def provider_config(self, type = None):
        self.option(str, 'target_protocol', 'http', help = 'Target protocol (http or https)')
        self.option(str, 'ssl_policy', 'ELBSecurityPolicy-2016-08', help = 'SSL policy definition')

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
        self.set('load_balancer', AWSApplicationLoadBalancerProvider)
        self.set('load_balancer_listener', AWSApplicationLoadBalancerListenerProvider)
