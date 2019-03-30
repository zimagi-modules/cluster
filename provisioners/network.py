from systems.command import profile


class Provisioner(profile.BaseProvisioner):

    def priority(self):
        return 2

    def ensure(self, name, config):
        provider = self.pop_value('provider', config)
        groups = self.pop_values('groups', config)

        if not provider:
            self.command.error("Network {} requires 'provider' field".format(name))

        self.exec('network save',
            network_provider_name =  provider,
            network_name = name,
            network_fields = self.interpolate(config,
                provider = provider
            ),
            group_names = groups,
            test = self.test
        )

    def variables(self, instance):
        return {
            'provider': instance.type,
            'groups': self.get_names(instance.groups)
        }

    def destroy(self, name, config):
        self.exec('network rm',
            network_name = name,
            force = True
        )
