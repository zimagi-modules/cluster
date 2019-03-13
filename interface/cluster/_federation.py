from systems.command.base import command_list
from systems.command.factory import resource
from systems.command.types import federation


class Command(federation.FederationRouterCommand):

    def get_command_name(self):
        return 'federation'

    def get_subcommands(self):
        base_name = self.get_command_name()
        return resource.ResourceCommandSet(
            federation.FederationActionCommand, base_name
        )
