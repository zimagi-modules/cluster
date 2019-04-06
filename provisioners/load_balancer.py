from systems.command import profile


class Provisioner(profile.BaseProvisioner):

    def priority(self):
        return 3

    def ensure(self, name, config):
        networks = self.pop_values('network', config)
        provider = self.pop_value('provider', config)
        listeners = self.pop_info('listeners', config)
        groups = self.pop_values('groups', config)
        firewalls = self.pop_values('firewalls', config)

        if not provider or not networks or not listeners:
            self.command.error("Load balancer {} requires 'network', 'provider', and 'listeners' fields".format(name))

        def process_network(network):
            self.exec('lb save',
                load_balancer_provider_name =  provider,
                load_balancer_name = name,
                load_balancer_fields = self.interpolate(config,
                    network = network,
                    provider = provider
                ),
                network_name = network,
                group_names = groups,
                firewall_names = firewalls,
                test = self.test
            )
            def process_listener(listener):
                self.exec('lb listener save',
                    load_balancer_name = name,
                    load_balancer_listener_name = listener,
                    load_balancer_listener_fields = self.interpolate(listeners[listener],
                        load_balancer = name,
                        network = network,
                        provider = provider
                    ),
                    test = self.test
                )
            if self.profile.include_inner('load_balancer_listener'):
                self.run_list(listeners.keys(), process_listener)

        self.run_list(networks, process_network)

    def scope(self, instance):
        return { 'network': instance.network.name }

    def variables(self, instance):
        variables = {
            'provider': instance.provider_type,
            'groups': self.get_names(instance.groups),
            'firewalls': self.get_names(instance.firewalls),
            'listeners': {}
        }
        for listener in instance.loadbalancerlistener_relation.all():
            variables['listeners'][listener.name] = self.get_variables(listener)

        return variables

    def destroy(self, name, config):
        networks = self.pop_values('network', config)

        def process_network(network):
            self.exec('lb rm',
                load_balancer_name = name,
                network_name = network,
                force = True
            )
        self.run_list(networks, process_network)
