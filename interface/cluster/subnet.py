from systems.command.factory import resource
from systems.command.types import subnet


class Command(subnet.SubnetRouterCommand):

    def get_subcommands(self):
        return resource.ResourceCommandSet(
            subnet.SubnetActionCommand, self.name,
            provider_name = 'network',
            provider_subtype = self.name
        )
