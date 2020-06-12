from systems.commands import profile


class ProfileComponent(profile.BaseProfileComponent):

    def priority(self):
        return 3

    def run(self, name, config):
        provider = self.pop_value('provider', config)
        networks = self.pop_values('network', config)
        groups = self.pop_values('groups', config)

        if not provider or not networks:
            self.command.error("Storage {} requires 'provider' and 'network' fields".format(name))

        def process(network):
            self.exec('storage save',
                storage_provider_name = provider,
                storage_name = name,
                storage_fields = self.interpolate(config,
                    network = network
                ),
                network_name = network,
                group_names = groups,
                test = self.test
            )
        self.run_list(networks, process)

    def scope(self, instance):
        return { 'network': instance.network.name }

    def variables(self, instance):
        return {
            'groups': self.get_names(instance.groups)
        }

    def destroy(self, name, config):
        networks = self.pop_values('network', config)

        def process_network(network):
            self.exec('storage remove',
                storage_name = name,
                network_name = network,
                force = True
            )
        self.run_list(networks, process_network)
