from systems.command.factory import resource
from systems.command.types import network


class Command(network.NetworkRouterCommand):

    def get_subcommands(self):
        return resource.ResourceCommandSet(
            network.NetworkActionCommand, self.name,
            provider_name = self.name,
            provider_subtype = self.name
        )
