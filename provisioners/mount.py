from systems.command import profile


class Provisioner(profile.BaseProvisioner):

    def priority(self):
        return 4

    def ensure(self, name, config):
        storage_sources = self.pop_values('storage', config)
        networks = self.pop_values('network', config)
        subnets = self.pop_values('subnet', config)
        groups = self.pop_values('groups', config)
        firewalls = self.pop_values('firewalls', config)

        if not storage_sources or not networks or not subnets:
            self.command.error("Storage mount {} requires 'storage', 'network', and 'subnet' fields".format(name))

        def process_storage(storage):
            def process_network(network):
                def process_subnet(subnet):
                    self.exec('mount save',
                        mount_name = name,
                        mount_fields = self.interpolate(config,
                            storage = storage,
                            network = network,
                            subnet = subnet
                        ),
                        storage_name = storage,
                        network_name = network,
                        subnet_name = subnet,
                        group_names = groups,
                        firewall_names = firewalls,
                        test = self.test
                    )
                self.run_list(subnets, process_subnet)
            self.run_list(networks, process_network)
        self.run_list(storage_sources, process_storage)

    def scope(self, instance):
        return {
            'storage': instance.storage.name,
            'network': instance.subnet.network.name,
            'subnet': instance.subnet.name
        }

    def variables(self, instance):
        return {
            'groups': self.get_names(instance.groups),
            'firewalls': self.get_names(instance.firewalls)
        }

    def destroy(self, name, config):
        storage_sources = self.pop_values('storage', config)
        networks = self.pop_values('network', config)
        subnets = self.pop_values('subnet', config)

        def process_storage(storage):
            def process_network(network):
                def process_subnet(subnet):
                    self.exec('mount rm',
                        mount_name = name,
                        storage_name = storage,
                        network_name = network,
                        subnet_name = subnet,
                        force = True
                    )
                self.run_list(subnets, process_subnet)
            self.run_list(networks, process_network)
        self.run_list(storage_sources, process_storage)
