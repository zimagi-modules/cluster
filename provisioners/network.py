from systems.command import profile


class Provisioner(profile.BaseProvisioner):

    def priority(self):
        return 1


    def ensure(self, name, config):
        provider = self.profile.pop_value('provider', config)
        groups = self.profile.pop_values('group_names', config)

        if not provider:
            self.command.error("Network {} requires 'provider' field".format(name))

        self.command.exec_local('network save', {
            'network_provider_name': provider,
            'network_name': name,
            'network_fields': config,
            'group_names': groups
        })


    def describe(self, network):
        return { 'provider': network.type }


    def destroy(self, name, config):
        self.command.exec_local('network rm', {
            'network_name': name,
            'force': True
        })
