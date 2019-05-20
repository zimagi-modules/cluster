from systems.command import profile


class ProfileComponent(profile.BaseProfileComponent):

    def priority(self):
        return 3

    def run(self, name, networks):
        self.exec('network peering save',
            network_peering_name = name,
            network_names = networks,
            test = self.test
        )

    def describe(self, instance):
        return self.get_names(instance.networks)

    def destroy(self, name, networks):
        self.exec('network peering rm',
            network_peering_name = name,
            force = True
        )
