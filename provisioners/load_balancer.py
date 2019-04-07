from systems.command import profile


class Provisioner(profile.BaseProvisioner):

    def priority(self):
        return 3

    def ensure(self, name, config):
        networks = self.pop_values('network', config)
        provider = self.pop_value('provider', config)
        domain = self.pop_value('domain', config)
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
                    provider = provider,
                    domain = domain
                ),
                network_name = network,
                domain_name = domain,
                group_names = groups,
                firewall_names = firewalls,
                test = self.test
            )
            def process_listener(listener):
                listener_config = listeners[listener]
                certificate = self.pop_value('certificate', listener_config)

                self.exec('lb listener save',
                    load_balancer_name = name,
                    load_balancer_listener_name = listener,
                    load_balancer_listener_fields = self.interpolate(listener_config,
                        load_balancer = name,
                        network = network,
                        provider = provider,
                        domain = domain
                    ),
                    network_name = network,
                    certificate_name = certificate,
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
        if instance.domain:
            variables['domain'] = instance.domain.name

        for listener in instance.loadbalancerlistener_relation.all():
            listener_config = self.get_variables(listener)

            if listener.certificate:
                listener_config['certificate'] = listener.certificate.name

            variables['listeners'][listener.name] = listener_config

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
