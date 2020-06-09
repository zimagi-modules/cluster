from systems.plugins.index import BaseProvider


class NetworkProvider(BaseProvider('network.network', 'aws')):

    def add_credentials(self, config):
        self.aws_credentials(config)

    def remove_credentials(self, config):
        self.clean_aws_credentials(config)


class SubnetProvider(BaseProvider('network.subnet', 'aws')):

    def add_credentials(self, config):
        self.aws_credentials(config)

    def remove_credentials(self, config):
        self.clean_aws_credentials(config)

    def initialize_terraform(self, instance, created):
        if instance.config['zone'] is None and instance.config['zone_suffix'] is not None:
            instance.config['zone'] = "{}{}".format(
                instance.network.config['region'],
                instance.config['zone_suffix']
            )
        super().initialize_terraform(instance, created)
        instance.variables['use_nat_route_table'] = True if instance.nat_subnet else False


class FirewallProvider(BaseProvider('network.firewall', 'aws')):

    def add_credentials(self, config):
        self.aws_credentials(config)

    def remove_credentials(self, config):
        self.clean_aws_credentials(config)

    def get_firewall_id(self):
        return self.instance.variables['security_group_id']


class FirewallRuleProvider(BaseProvider('network.firewall_rule', 'aws')):

    def add_credentials(self, config):
        self.aws_credentials(config)

    def remove_credentials(self, config):
        self.clean_aws_credentials(config)
