from systems.command import profile


class Provisioner(profile.BaseProvisioner):

    def priority(self):
        return 3

    def ensure(self, name, config):
        networks = self.pop_values('network', config)
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
                    provider = provider
                ),
                network_name = network,
                group_names = groups,
                test = self.test
            )
        self.run_list(networks, process_network)

    def scope(self, instance):
        return { 'network': instance.network.name }

    def variables(self, instance):
        return {
            'provider': instance.provider_type,
            'groups': self.get_names(instance.groups)
        }

    def destroy(self, name, config):
        networks = self.pop_values('network', config)

        def process_network(network):
            self.exec('cert rm',
                certificate_name = name,
                network_name = network,
                force = True
            )
        self.run_list(networks, process_network)
