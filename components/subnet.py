from systems.command import profile


class ProfileComponent(profile.BaseProfileComponent):

    def priority(self):
        return 3

    def run(self, name, config):
        networks = self.pop_values('network', config)
        groups = self.pop_values('groups', config)

        if not networks:
            self.command.error("Subnet {} requires 'network' field".format(name))

        def process(network):
            self.exec('subnet save',
                subnet_name = name,
                subnet_fields = self.interpolate(config,
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
            self.exec('subnet rm',
                subnet_name = name,
                network_name = network,
                force = True
            )
        self.run_list(networks, process_network)
