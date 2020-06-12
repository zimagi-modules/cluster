from systems.commands import profile


class ProfileComponent(profile.BaseProfileComponent):

    def priority(self):
        return 3

    def run(self, name, config):
        networks = self.pop_values('network', config)
        domain = self.pop_value('domain', config)
        provider = self.pop_value('provider', config)
        groups = self.pop_values('groups', config)

        if not provider:
            self.command.error("Certificate {} requires 'network' and 'provider' fields".format(name))

        def process_network(network):
            self.exec('cert save',
                certificate_provider_name =  provider,
                certificate_name = name,
                certificate_fields = self.interpolate(config,
                    network = network,
                    domain = domain,
                    provider = provider
                ),
                network_name = network,
                domain_name = domain,
                group_names = groups,
                test = self.test
            )
        self.run_list(networks, process_network)

    def scope(self, instance):
        return { 'network': instance.network.name }

    def variables(self, instance):
        return {
            'provider': instance.provider_type,
            'domain': instance.domain.name if instance.domain else None,
            'groups': self.get_names(instance.groups)
        }

    def destroy(self, name, config):
        networks = self.pop_values('network', config)

        def process_network(network):
            self.exec('cert remove',
                certificate_name = name,
                network_name = network,
                force = True
            )
        self.run_list(networks, process_network)
