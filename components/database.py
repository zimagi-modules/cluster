from systems.commands import profile


class ProfileComponent(profile.BaseProfileComponent):

    def priority(self):
        return 7

    def run(self, name, config):
        networks = self.pop_values('network', config)
        subnets = self.pop_values('subnets', config)
        provider = self.pop_value('provider', config)
        domain = self.pop_value('domain', config)
        groups = self.pop_values('groups', config)
        firewalls = self.pop_values('firewalls', config)

        if not provider or not networks:
            self.command.error("Database {} requires 'network' and 'provider' fields".format(name))

        def process_network(network):
            self.exec('database save',
                database_provider_name =  provider,
                database_name = name,
                database_fields = self.interpolate(config,
                    network = network,
                    provider = provider,
                    domain = domain
                ),
                network_name = network,
                subnet_names = subnets,
                domain_name = domain,
                group_names = groups,
                firewall_names = firewalls,
                test = self.test
            )

        self.run_list(networks, process_network)

    def scope(self, instance):
        return { 'network': instance.network.name }

    def variables(self, instance):
        variables = {
            'provider': instance.provider_type,
            'groups': self.get_names(instance.groups),
            'subnets': self.get_names(instance.subnets),
            'firewalls': self.get_names(instance.firewalls),
        }
        if instance.domain:
            variables['domain'] = instance.domain.name

        return variables

    def destroy(self, name, config):
        networks = self.pop_values('network', config)

        def process_network(network):
            self.exec('database remove',
                database_name = name,
                network_name = network,
                force = True
            )
        self.run_list(networks, process_network)
