from systems.command import profile


class Provisioner(profile.BaseProvisioner):

    def priority(self):
        return 6

    def ensure(self, name, config):
        provider = self.pop_value('provider', config)
        count = self.pop_value('count', config)
        networks = self.pop_values('network', config)
        subnets = self.pop_values('subnet', config)
        load_balancer = self.pop_value('load_balancer', config)
        load_balancer_listener = self.pop_value('load_balancer_listener', config)
        groups = self.pop_values('groups', config)
        firewalls = self.pop_values('firewalls', config)
        volumes = self.pop_info('volumes', config)

        if not provider or not networks or not subnets:
            self.command.error("Server {} requires 'provider', 'network', and 'subnet' fields".format(name))

        if load_balancer and not load_balancer_listener or not load_balancer and load_balancer_listener:
            self.command.error("Server {} requires neither or both of 'load_balancer' and 'load_balancer_listener' fields".format(name))

        if not count:
            count = 1

        def process_network(network):
            def process_subnet(subnet):
                self.exec('server save',
                    count = count,
                    server_provider_name = provider,
                    server_name = name,
                    server_fields = self.interpolate(config,
                        provider = provider,
                        network = network,
                        subnet = subnet,
                        load_balancer = load_balancer
                    ),
                    network_name = network,
                    subnet_name = subnet,
                    load_balancer_name = load_balancer,
                    load_balancer_listener_name = load_balancer_listener,
                    group_names = groups,
                    firewall_names = firewalls,
                    remove = True,
                    test = self.test
                )
                def process_volume(volume):
                    volume_provider = self.get_value('provider', volumes[volume])
                    volume_fields = self.interpolate(volumes[volume],
                        server_provider = provider,
                        volume_provider = volume_provider,
                        network = network,
                        subnet = subnet
                    )
                    volume_fields.pop('provider')

                    def process_volume_server(index):
                        self.exec('server volume save',
                            server_volume_provider_name = volume_provider,
                            server_volume_name = volume,
                            server_volume_fields = volume_fields,
                            network_name = network,
                            subnet_name = subnet,
                            server_name = "{}{}".format(name, index),
                            test = self.test
                        )
                    self.run_list(range(1, count + 1), process_volume_server)

                if volumes and self.profile.include_inner('server_volume'):
                    self.run_list(volumes.keys(), process_volume)
            self.run_list(subnets, process_subnet)
        self.run_list(networks, process_network)

    def scope(self, instance):
        return {
            'network': instance.subnet.network.name,
            'subnet': instance.subnet.name
        }

    def variables(self, instance):
        variables = {
            'provider': instance.provider_type,
            'groups': self.get_names(instance.groups),
            'firewalls': self.get_names(instance.firewalls),
            'volumes': {}
        }
        if instance.load_balancer:
            variables['load_balancer'] = instance.load_balancer.name

        if instance.load_balancer_listener:
            variables['load_balancer_listener'] = instance.load_balancer_listener.name

        for volume in instance.servervolume_relation.all():
            volume_config = self.get_variables(volume)
            volume_config['provider'] = volume.provider_type
            variables['volumes'][volume.name] = volume_config

        return variables

    def destroy(self, name, config):
        networks = self.pop_values('network', config)
        subnets = self.pop_values('subnet', config)

        def process_network(network):
            def process_subnet(subnet):
                self.exec('server rm',
                    server_name = name,
                    network_name = network,
                    subnet_name = subnet,
                    force = True
                )
            self.run_list(subnets, process_subnet)
        self.run_list(networks, process_network)
