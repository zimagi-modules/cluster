from systems.plugins.index import BaseProvider


class LoadBalancerProvider(BaseProvider('load_balancer.load_balancer', 'aws_application')):

    def add_credentials(self, config):
        self.aws_credentials(config)

    def remove_credentials(self, config):
        self.clean_aws_credentials(config)

    def initialize_terraform(self, instance, created):
        relations = self.command.get_relations(instance.facade)
        super().initialize_terraform(instance, created)

        instance.config['subnets'] = self.get_subnets(relations['subnets'], instance.network)
        instance.config['security_groups'] = self.get_security_groups(relations['firewalls'], instance.firewalls)


class LoadBalancerListenerProvider(BaseProvider('load_balancer.load_balancer_listener', 'aws_application')):

    def add_credentials(self, config):
        self.aws_credentials(config)

    def remove_credentials(self, config):
        self.clean_aws_credentials(config)
