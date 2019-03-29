from systems.command import profile


class Provisioner(profile.BaseProvisioner):

    def priority(self):
        return 2

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

    def variables(self, instance):
        return {
            'provider': instance.type,
            'group_names': [ x.name for x in instance.groups.all() ]
        }

    def destroy(self, name, config):
        self.command.exec_local('network rm', {
            'network_name': name,
            'force': True
        })
