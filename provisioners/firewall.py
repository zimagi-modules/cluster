from systems.command import profile


class Provisioner(profile.BaseProvisioner):

    def priority(self):
        return 3

    def ensure(self, name, config):
        networks = self.profile.pop_values('network', config)
        rules = self.profile.pop_info('rules', config)
        groups = self.profile.pop_values('group_names', config)

        def process(network):
            self.command.exec_local('firewall save', {
                'network_name': network,
                'firewall_name': name,
                'firewall_fields': config,
                'group_names': groups
            })
            def process_rule(rule):
                self.command.exec_local('firewall rule save', {
                    'network_name': network,
                    'firewall_name': name,
                    'firewall_rule_name': rule,
                    'firewall_rule_fields': rules[rule]
                })
            self.command.run_list(rules.keys(), process_rule)

        if not networks:
            self.command.error("Firewall {} requires 'network' field".format(name))

        if not rules:
            self.command.error("Firewall {} requires 'rules' field defined".format(name))

        self.command.run_list(networks, process)

    def scope(self, instance):
        return { 'network': instance.network.name }

    def variables(self, instance):
        variables = {
            'group_names': [ x.name for x in instance.groups.all() ],
            'rules': {}
        }
        for rule in instance.firewallrule_relation.all():
            variables['rules'][rule.name] = self.profile.get_variables(rule)

        return variables
