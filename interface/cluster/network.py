from systems.command.base import command_list
from systems.command.factory import resource, router
from systems.command.types import network


class Command(network.NetworkRouterCommand):

    def get_subcommands(self):
        network_peering_name = 'network_peering'

        return command_list(
            resource.ResourceCommandSet(
                network.NetworkActionCommand, self.name,
                provider_name = self.name,
                provider_subtype = self.name
            ),
            ('peering', router.Router(
                network.NetworkRouterCommand,
                resource.ResourceCommandSet(
                    network.NetworkActionCommand, network_peering_name,
                    provider_name = network_peering_name,
                    provider_subtype = network_peering_name
                )
            ))
        )
